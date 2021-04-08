import os
from pyflame import filemodification
import shutil
import subprocess
import sys
from pyflame import datacollection
import numpy as np
from pyflame import plotting
from pyflame import plotting_sns
from multiprocessing import Pool
import time
from pyflame import tables
import scipy.stats.stats as stats
from pyflame import utils
import yaml
import pickle
from pathlib import Path
import pandas as pd

class FlameSession:

    def __init__(self, config_file):
        config = yaml.load(open(config_file), Loader=yaml.FullLoader)

        self.model_xml = config["model_xml"]
        self.model_path = config["model_path"]
        self.xparser_path = config["xparser_path"]
        self.workspace = config["workspace"]
        self.base_xml = config["base_xml"]
        self.iterations = config["iterations"]
        self.output_frequency = config["output_frequency"]
        self.no_runs = config["runs"]
        self.run_aggregation = config["run_aggregation"]

        if "run_aggregation" in config:
            self.run_aggregation = config["run_aggregation"]
        else:
            self.run_aggregation = ["SINGLE", "MEAN"]

        if "agent_histogram_frequency" in config:
            self.agent_histogram_frequency = config["agent_histogram_frequency"]
        else:
            self.agent_histogram_frequency = 99999999999999999

        if "transient" in config:
            self.transient = config["transient"]
        else:
            self.transient = 0

        if "burn_in_its" in config:
            self.burn_in_its = config["burn_in_its"]
        else:
            self.burn_in_its = 0

        self.experiments = config["experiments"]

        if "capture_data_only" in config:
            self.capture_data_only = config["capture_data_only"]
        else:
            self.time_series = {}

        if "time_series" in config:
            self.time_series = config["time_series"]
        else:
            self.time_series = {}

        if "single_agent_time_series" in config:
            self.agent_time_series = config["single_agent_time_series"]
        else:
            self.agent_time_series = {}

        if "agent_histogram" in config:
            self.agent_histogram = config["agent_histogram"]
        else:
            self.agent_histogram = {}

        if "overtime_histogram" in config:
            self.overtime_histogram = config["overtime_histogram"]
        else:
            self.overtime_histogram = {}

        if "correlation_matrix" in config:
            self.correlation_matrix = config["correlation_matrix"]
        else:
            self.correlation_matrix = {}

        if "correlation_table" in config:
            self.correlation_table = config["correlation_table"]
        else:
            self.correlation_table = {}

        self.variables = {}

        for agent in self.capture_data_only:
            if agent not in self.variables:
                self.variables[agent] = set()
            self.variables[agent].update(self.capture_data_only[agent])
            self.variables[agent].add('id')
        for agent in self.time_series:
            if agent not in self.variables:
                self.variables[agent] = set()
            self.variables[agent].update(self.time_series[agent])
            self.variables[agent].add('id')
        for agent in self.agent_time_series:
            if agent not in self.variables:
                self.variables[agent] = set()
            self.variables[agent].update(self.agent_time_series[agent])
            self.variables[agent].add('id')
        for agent in self.agent_histogram:
            if agent not in self.variables:
                self.variables[agent] = set()
            self.variables[agent].update(self.agent_histogram[agent])
            self.variables[agent].add('id')
        for agent in self.overtime_histogram:
            if agent not in self.variables:
                self.variables[agent] = set()
            self.variables[agent].update(self.overtime_histogram[agent])
            self.variables[agent].add('id')
        for c in self.correlation_matrix:
            for agent in self.correlation_matrix[c]:
                if agent not in self.variables:
                    self.variables[agent] = set()
                self.variables[agent].update(self.correlation_matrix[c][agent])
                self.variables[agent].add('id')
        for t in self.correlation_table:
            for l in self.correlation_table[t]:
                for e in l:
                    for agent in e:
                        if agent not in self.variables:
                            self.variables[agent] = set()
                        self.variables[agent].add(e[agent])
                        self.variables[agent].add('id')

        self.run_folder = self.workspace + "/RUNS/"
        self.plot_folder = self.workspace + "/RESULTS/"
        self.table_folder = self.workspace + "/RESULTS/"
        self.matrix_folder = self.workspace + "/RESULTS/"
        self.transient_folder = self.workspace + "/TRANSIENT/"

    def run_model(self, workspace, job, its, freq, sleep=0, initial_state="0.xml"):
        time.sleep(sleep)
        print("  " + job, flush=True)
        folder = workspace + "/" + job

        with open(folder + "/out.txt", "wb") as out, open(folder + "/err.txt", "wb") as err:
            subprocess.run([self.model_path + "/main", str(its), folder + "/" + initial_state, "-f", str(freq)],
                           stdout=out, stderr=err)

    def parse_model(self):
        print("Parsing model structure...", end="")
        utils.create_folder(self.workspace)
        sys.stdout.flush()
        os.chdir(self.xparser_path)
        with open(self.workspace + "/xparser-out.txt", "wb") as out, open(self.workspace + "/xparser-err.txt", "wb") as err:
            subprocess.run(["./xparser", self.model_xml], stdout=out, stderr=err)
        print(" DONE")

    def compile_model(self):
        utils.create_folder(self.workspace)
        print("Compiling model code...", end="", flush=True)
        os.chdir(self.model_path)
        with open(self.workspace + "/compiler-out.txt", "wb") as out, open(self.workspace + "/compiler-err.txt", "wb") as err:
            subprocess.run("make", stdout=out, stderr=err)
        print(" DONE")

    def modify_xml(self):
        print("Modifying xml.c...", end="", flush=True)
        filemodification.modifyXMLdotC(self.model_path, self.variables)
        print(" DONE")

    def simulate_model_transient(self, no_cpus, skip=False):
        utils.create_folder(self.workspace)

        if not skip:
            utils.delete_folder(self.transient_folder)

        job_list = []
        for i in range(0, self.no_runs):
            base_folder = self.transient_folder + "/" + str(i) + "/"
            if not os.path.exists(base_folder):
                utils.create_folder(base_folder)
                shutil.copyfile(self.base_xml, base_folder + "0.xml")
                if self.transient > 0:
                    job_list.append(str(i))

        print("Running transient simulations...")
        pool = Pool(processes=no_cpus)
        c = 0.0
        for job in job_list:
            pool.apply_async(self.run_model, (self.transient_folder, job, self.transient, self.transient, c))
            c = (c + 1) % no_cpus

        pool.close()
        pool.join()
        print(" DONE")

    def simulate_model(self, no_cpus, skip=False):
        utils.create_folder(self.workspace)

        # Create folder structure and 0.xml files
        if not skip:
            utils.delete_folder(self.run_folder)

        job_list = []
        for e in self.experiments:
            for i in range(0, self.no_runs):
                base_folder = self.run_folder + e + "/" + str(i) + "/"
                if not os.path.exists(base_folder):
                    utils.create_folder(base_folder)
                    shutil.copyfile(self.transient_folder + "/" + str(i) + "/" + str(self.transient) + ".xml", base_folder + str(self.transient) + ".xml")
                    filemodification.modify0xml(base_folder + str(self.transient) + ".xml", self.experiments[e])
                    job_list.append(e + "/" + str(i))

        # Run model
        print("Running Experiments...", flush=True)
        pool = Pool(processes=no_cpus)

        c = 0.0
        for job in job_list:
            pool.apply_async(self.run_model, (self.run_folder, job, self.iterations, self.output_frequency, c, str(self.transient) + ".xml"))
            c = (c + 1) % no_cpus

        pool.close()
        pool.join()
        print(" DONE")

    def build_and_run(self, no_cpus, skip=False):
        self.parse_model()
        self.compile_model()
        self.simulate_model_transient(no_cpus, skip)
        self.modify_xml()
        self.compile_model()
        self.simulate_model(no_cpus, skip)

    def load_simulated_data(self):
        print("Reading and aggregating data... ", flush=True)
        self.aggregated_data = {}
        self.disaggregated_data = {}
        self.single_ids = set()
        self.aggregated_ids = set()
        for e in self.experiments:
            print("  " + e)
            run_data_agents_aggregated = []
            run_data = []
            for i in range(0, self.no_runs):
                print("    " + str(i+1) + "/" + str(self.no_runs), flush=True)
                single_run = datacollection.collect_run(self.workspace + "/RUNS/" + e + "/" + str(i) + "/", self.variables, self.burn_in_its, 1000000000)
                run_data.append(single_run)
                run_data_agents_aggregated.append(datacollection.aggregate_agents(single_run, lambda x: np.mean(x)))

                self.aggregated_data[e] = {}
            for agg in self.run_aggregation:
                if agg == "MEAN":
                    self.aggregated_data[e][agg] = datacollection.aggregate_runs(run_data_agents_aggregated, lambda x: np.mean(x, axis=0))
                    self.aggregated_ids.add(agg)
                elif agg == "MEDIAN":
                    self.aggregated_data[e][agg] = datacollection.aggregate_runs(run_data_agents_aggregated, lambda x: np.median(x, axis=0))
                    self.aggregated_ids.add(agg)
                elif agg == "SINGLE":
                    for i in range(0, self.no_runs):
                        self.aggregated_data[e][i] = run_data_agents_aggregated[i]
                        self.single_ids.add(i)
                else:
                    sys.stderr.write(" ERROR: Aggregation method " + agg + " not supported!\n")

            self.disaggregated_data[e] = {}
            for i in range(0, self.no_runs):
                self.disaggregated_data[e][i] = run_data[i]

        print(" DONE")

    def cache_file_exists(self):
        cache_file = self.workspace + "/cache.bin"

        return Path(cache_file).exists()

    def write_data_to_cache(self):
        print("Writing data to cache file... ", end="", flush=True)
        cache_file = self.workspace + "/cache.bin"

        data = {}
        data['aggregated_data'] = self.aggregated_data
        data['disaggregated_data'] = self.disaggregated_data
        data['single_ids'] = self.single_ids
        data['aggregated_ids'] = self.aggregated_ids

        pickle.dump(data, open(cache_file, "wb"))

        print(" DONE")

    def load_data_from_cache(self):
        print("Loading data from cache file... ", end="", flush=True)

        cache_file = self.workspace + "/cache.bin"
        data = pickle.load(open(cache_file, "rb"))

        self.aggregated_data = data['aggregated_data']
        self.disaggregated_data = data['disaggregated_data']
        self.single_ids = data['single_ids']
        self.aggregated_ids = data['aggregated_ids']

        print(" DONE")

    def generate_time_series_plot(self, agent, var, experiments, run_ids, agents_aggregated=True, save_as_csv=False, save_as_png=False, show_plot=False, linewidth=1):
        
        plot_style = 'default'
        #plot_style = 'sns'
        
        #print("Trying: set DataFrame")
        #indices: [e][id][agent][var]
        #shapes: [experiments][run_ids][agent][var]
        print("experiments: " + str(experiments) + ", dtype: " + str(type(experiments)) + ", dtype elements: " + str(type(experiments[0])) + ", len: " + str(len(experiments)))
        print("run_ids: " + str(run_ids) + ", dtype: " + str(type(run_ids)) + ", dtype elements: " + str(type(run_ids[0])) + ", len: " + str(len(run_ids)))
        df = pd.DataFrame(data=np.zeros((len(experiments),len(run_ids))), columns = experiments, index = [run_ids, agent, var])
        print("df.shape:")
        print(df.shape) 
        print("df.index:")
        print(df.index) 
        
        data_full = []
        labels = []
        for e in experiments:
            #print("start: experiment " + e)
            data = []
            labels.append(e)
            for id in run_ids:
                print("Run: " + str(id))                
                if agents_aggregated:
                    print("\t\tagents_aggregated")
                    #print(self.aggregated_data)
                    print(self.aggregated_data[e][id][agent][var])
                    data.append(self.aggregated_data[e][id][agent][var])
                    #df.loc[e,id,agent,var] = self.aggregated_data[e][id][agent][var]
                else:
                    print("\t\t!agents_aggregated")
                    #print(self.disaggregated_data)
                    transposed = np.transpose(self.disaggregated_data[e][id][agent][var])
                    for ts in transposed:
                        data.append(ts)
                        #df.loc[e,id,agent,var] = ts
                        
            data_full.append(data)
            print("\t data_fill after step: experiment " + e)
            print(data_full)
            
        print("After experiments loop:")
        print(data_full)
            
        #test
        #print("data_full.len():") 
        #print(len(data_full), flush=True)
        #print(dir(data_full)) 
        #print(data_full)

        #print("Trying: set DataFrame")    
        #print(df)
        #print("df.shape:")
        #print(df.shape) 
        
        
        if show_plot or save_as_png:
            if plot_style == 'default':
                plotting.timeseries_plot(data_full, labels, agent + ": " + var, linewidth, save_as_png, show_plot)
            elif plot_style == 'sns':
                plotting_sns.timeseries_plot(data_full, labels, agent + ": " + var, linewidth, save_as_png, show_plot)
            else:
                raise Exception("Timeseries plot failed")
                
        if save_as_csv:
            tables.write_dataseries_csv(data_full, labels, save_as_csv)

    def generate_agent_histogram_plot(self, agent, var, experiments, run_ids, snap_ids, save_as_csv=False, save_as_png=False, show_plot=False):
        data = []
        labels = []
        for e in experiments:
            agg_data = []
            for run_id in run_ids:
                for snap_id in snap_ids:
                    agg_data.append(self.disaggregated_data[e][run_id][agent][var][snap_id])
            data.append(list(np.array(agg_data).flat))
            labels.append(e)

        if show_plot or save_as_png:
            plotting.histogram_plot(data, labels, agent + ": " + var, save_as_file=save_as_png, show=show_plot)

        if save_as_csv:
            tables.write_dataseries_csv(list(map(lambda d: [d], data)), labels, save_as_csv)

    def generate_overtime_histogram_plot(self, agent, var, experiments, run_ids, save_as_csv=False, save_as_png=False, show_plot=False):
        data = []
        labels = []
        for e in experiments:
            agg_data = []
            for run_id in run_ids:
                agg_data.append(self.disaggregated_data[e][run_id][agent][var])
            data.append(list(np.array(agg_data).flat))
            labels.append(e)

        if show_plot or save_as_png:
            plotting.histogram_plot(data, labels, agent + ": " + var, save_as_file=save_as_png, show=show_plot)

        if save_as_csv:
            tables.write_dataseries_csv(list(map(lambda d: [d], data)), labels, save_as_csv)

    def generate_correlation_table(self, table_entries, experiments, run_ids, agg_function=(lambda x: np.mean(x, axis=0)), save_as_csv=False, save_as_txt=False, show_table=False):
        all_corrs = []

        first_row = []
        for entry in table_entries:
            first_row.append(utils.get_label_from_corr_pair(entry))

        for entry in table_entries:
            corr_row = []
            header = []
            for e in experiments:
                header.append(e)
                corrs = []
                for id in run_ids:
                    data = []
                    for ee in entry:
                        for agent in ee:
                            var = ee[agent]
                            data.append(self.aggregated_data[e][id][agent][var])
                    corrs.append(np.corrcoef(data)[0][1])
                agg_corr = agg_function(corrs)
                corr_row.append(agg_corr)
            all_corrs.append(corr_row)

        tables.write_corr_table(all_corrs, header, first_row, save_as_file=save_as_txt, show=show_table)

        if save_as_csv:
            tables.write_corr_table_csv(all_corrs, header, first_row, save_as_csv)

    def generate_correlation_barchart(self, corr_pair, experiments, run_ids, save_as_png=False, show_plot=False):
        title = utils.get_label_from_corr_pair(corr_pair)

        all_corrs = []
        all_p_values = []
        labels=[]
        for e in experiments:
            labels.append(e)
            corrs = []
            p_values = []
            for id in run_ids:
                data = []
                for ee in corr_pair:
                    for agent in ee:
                        var = ee[agent]
                        data.append(self.aggregated_data[e][id][agent][var])
                pr = stats.pearsonr(data[0],data[1])
                corrs.append(pr[0])
                p_values.append(pr[1]/2)
            all_corrs.append(corrs)
            all_p_values.append(p_values)

        plotting.barchart_plot(all_corrs, labels, title, errors=all_p_values, save_as_file=save_as_png, show=show_plot)
