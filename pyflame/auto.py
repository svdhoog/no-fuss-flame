from pyflame import utils


def generate_single_run_time_series_plots(nff_session, csv=True, plot=True):
    print("Generating single run time series plots...", flush=True)
    for agent in nff_session.time_series:
        for var in nff_session.time_series[agent]:
            print("  " + agent + "." + var, flush=True)
            for e in nff_session.experiments:
                for id in nff_session.single_ids:
                    folder = nff_session.plot_folder + "/TIME_SERIES/INDIVIDUAL/" + e + "/" + str(id) + "/" + agent + "/"
                    utils.create_folder(folder)

                    if plot:
                        save_as_png = (folder + var)
                    else:
                        save_as_png = False
                    if csv:
                        save_as_csv = (folder + var)
                    else:
                        save_as_csv = False

                    try:
                        nff_session.generate_time_series_plot(agent, var, [e], [id], save_as_png=save_as_png, save_as_csv=save_as_csv)
                    except:
                        print("  ERROR: ", agent, var, e, id)

    print(" DONE")


def generate_aggregated_time_series_plots(nff_session, csv=True, plot=True):
    print("Generating aggregated time series plots...", flush=True)
    for agent in nff_session.time_series:
        for var in nff_session.time_series[agent]:
            print("  " + agent + "." + var, flush=True)
            for e in nff_session.experiments:
                for id in nff_session.aggregated_ids:
                    folder = nff_session.plot_folder + "/TIME_SERIES/INDIVIDUAL/" + e + "/" + str(id) + "/" + agent + "/"
                    utils.create_folder(folder)

                    if plot:
                        save_as_png = (folder + var)
                    else:
                        save_as_png = False
                    if csv:
                        save_as_csv = (folder + var)
                    else:
                        save_as_csv = False

                    try:
                        nff_session.generate_time_series_plot(agent, var, [e], [id], save_as_png=save_as_png, save_as_csv=save_as_csv)
                    except:
                        print("  ERROR: ", agent, var, e, id)
    print(" DONE")


def generate_single_run_time_series_plots_combined(nff_session, csv=True, plot=True):
    print("Generating combined single run time series plots...", flush=True)
    for agent in nff_session.time_series:
        for var in nff_session.time_series[agent]:
            print("  " + agent + "." + var, flush=True)
            for id in nff_session.single_ids:
                folder = nff_session.plot_folder + "/TIME_SERIES/COMBINED/" + str(id) + "/" + agent + "/"
                utils.create_folder(folder)

                if plot:
                    save_as_png = (folder + var)
                else:
                    save_as_png = False
                if csv:
                    save_as_csv = (folder + var)
                else:
                    save_as_csv = False

                try:
                    nff_session.generate_time_series_plot(agent, var, nff_session.experiments, [id], save_as_png=save_as_png, save_as_csv=save_as_csv)
                except:
                    print("  ERROR: ", agent, var, id)
    print(" DONE")


def generate_aggregated_time_series_plots_combined(nff_session, csv=True, plot=True):
    print("Generating combined aggregated time series plots...", flush=True)
    for agent in nff_session.time_series:
        for var in nff_session.time_series[agent]:
            print("  " + agent + "." + var, flush=True)
            for id in nff_session.aggregated_ids:
                folder = nff_session.plot_folder + "/TIME_SERIES/COMBINED/" + str(id) + "/" + agent + "/"
                utils.create_folder(folder)

                if plot:
                    save_as_png = (folder + var)
                else:
                    save_as_png = False
                if csv:
                    save_as_csv = (folder + var)
                else:
                    save_as_csv = False

                try:
                    nff_session.generate_time_series_plot(agent, var, nff_session.experiments, [id], save_as_png=save_as_png, save_as_csv=save_as_csv)
                except:
                    print("  ERROR: ", agent, var, id)
    print(" DONE")


def generate_all_runs_time_series_plots(nff_session, csv=True, plot=True):
    print("Generating all runs time series plots...", flush=True)
    for agent in nff_session.time_series:
        for var in nff_session.time_series[agent]:
            print("  " + agent + "." + var, flush=True)
            for e in nff_session.experiments:
                folder = nff_session.plot_folder + "/TIME_SERIES/INDIVIDUAL/" + e + "/ALL/" + agent + "/"
                utils.create_folder(folder)

                if plot:
                    save_as_png = (folder + var)
                else:
                    save_as_png = False
                if csv:
                    save_as_csv = (folder + var)
                else:
                    save_as_csv = False

                try:
                    nff_session.generate_time_series_plot(agent, var, [e], nff_session.single_ids, save_as_png=save_as_png, save_as_csv=save_as_csv, linewidth=0.5)
                except:
                    print("  ERROR: ", agent, var, e)
    print(" DONE")


def generate_all_runs_time_series_plots_combined(nff_session, csv=True, plot=True):
    print("Generating combined all runs time series plots...", flush=True)
    for agent in nff_session.time_series:
        for var in nff_session.time_series[agent]:
            print("  " + agent + "." + var, flush=True)
            folder = nff_session.plot_folder + "/TIME_SERIES/COMBINED/ALL/" + agent + "/"
            utils.create_folder(folder)

            if plot:
                save_as_png = (folder + var)
            else:
                save_as_png = False
            if csv:
                save_as_csv = (folder + var)
            else:
                save_as_csv = False

            try:
                nff_session.generate_time_series_plot(agent, var, nff_session.experiments, nff_session.single_ids, save_as_png=save_as_png, save_as_csv=save_as_csv, linewidth=0.5)
            except:
                print("  ERROR: ", agent, var)
    print(" DONE")


def generate_single_agent_time_series_plots(nff_session, csv=True, plot=True):
    print("Generating single agent time series plots...", flush=True)
    for agent in nff_session.agent_time_series:
        for var in nff_session.agent_time_series[agent]:
            print("  " + agent + "." + var, flush=True)
            for e in nff_session.experiments:
                for id in nff_session.single_ids:
                    folder = nff_session.plot_folder + "/TIME_SERIES/INDIVIDUAL/" + e + "/" + str(id) + "/" + agent + "_SINGLE/"
                    utils.create_folder(folder)

                    if plot:
                        save_as_png = (folder + var)
                    else:
                        save_as_png = False
                    if csv:
                        save_as_csv = (folder + var)
                    else:
                        save_as_csv = False

                    try:
                        nff_session.generate_time_series_plot(agent, var, [e], [id], save_as_png=save_as_png, save_as_csv=save_as_csv, agents_aggregated=False, linewidth=0.5)
                    except:
                        print("  ERROR: ", agent, var, e, id)
    print(" DONE")


def generate_single_agent_time_series_plots_combined(nff_session, csv=True, plot=True):
    print("Generating single agent time series plots...", flush=True)
    for agent in nff_session.agent_time_series:
        for var in nff_session.agent_time_series[agent]:
            print("  " + agent + "." + var, flush=True)
            for id in nff_session.single_ids:
                folder = nff_session.plot_folder + "/TIME_SERIES/COMBINED/" + str(id) + "/" + agent + "_SINGLE/"
                utils.create_folder(folder)

                if plot:
                    save_as_png = (folder + var)
                else:
                    save_as_png = False
                if csv:
                    save_as_csv = (folder + var)
                else:
                    save_as_csv = False
                try:
                    nff_session.generate_time_series_plot(agent, var, nff_session.experiments, [id], save_as_png=save_as_png, save_as_csv=save_as_csv, agents_aggregated=False, linewidth=0.5)
                except:
                    print("  ERROR: ", agent, var, id)
    print(" DONE")


def generate_agent_histograms_single_runs(nff_session, csv=True, plot=True):
    print("Generating single run agent histograms...", flush=True)
    for agent in nff_session.agent_histogram:
        for var in nff_session.agent_histogram[agent]:
            print("  " + agent + "." + var, flush=True)
            for e in nff_session.experiments:
                for id in nff_session.single_ids:
                    for t in map(lambda x: int(x * nff_session.agent_histogram_frequency / nff_session.output_frequency), range(0, int((nff_session.iterations-nff_session.burn_in_its) / nff_session.agent_histogram_frequency))):
                        folder = nff_session.plot_folder + "/HISTOGRAM/AGENT/INDIVIDUAL/" + e + "/" + str(id) + "/" + agent + "/" + var + "/"
                        utils.create_folder(folder)

                        if plot:
                            save_as_png = (folder + str(t * nff_session.output_frequency))
                        else:
                            save_as_png = False
                        if csv:
                            save_as_csv = (folder + str(t * nff_session.output_frequency))
                        else:
                            save_as_csv = False
                        try:
                            nff_session.generate_agent_histogram_plot(agent, var, [e], [id], [t], save_as_png=save_as_png, save_as_csv=save_as_csv)
                        except:
                            print("  ERROR: ", agent, var, e, id, t)
    print(" DONE")


def generate_agent_histograms_single_runs_combined(nff_session, csv=True, plot=True):
    print("Generating single run combined agent histograms...", flush=True)
    for agent in nff_session.agent_histogram:
        for var in nff_session.agent_histogram[agent]:
            print("  " + agent + "." + var, flush=True)
            for id in nff_session.single_ids:
                for t in map(lambda x: int(x * nff_session.agent_histogram_frequency / nff_session.output_frequency), range(0, int((nff_session.iterations-nff_session.burn_in_its) / nff_session.agent_histogram_frequency))):
                    folder = nff_session.plot_folder + "/HISTOGRAM/AGENT/COMBINED/" + str(id) + "/" + agent + "/" + var + "/"
                    utils.create_folder(folder)

                    if plot:
                        save_as_png = (folder + str(t * nff_session.output_frequency))
                    else:
                        save_as_png = False
                    if csv:
                        save_as_csv = (folder + str(t * nff_session.output_frequency))
                    else:
                        save_as_csv = False

                    try:
                        nff_session.generate_agent_histogram_plot(agent, var, nff_session.experiments, [id], [t], save_as_png=save_as_png, save_as_csv=save_as_csv)
                    except:
                        print("  ERROR: ", agent, var, id, t)
    print(" DONE")


def generate_agent_histograms_aggregated(nff_session, csv=True, plot=True):
    print("Generating aggregated agent histograms...", flush=True)
    for agent in nff_session.agent_histogram:
        for var in nff_session.agent_histogram[agent]:
            print("  " + agent + "." + var, flush=True)
            for e in nff_session.experiments:
                for t in map(lambda x: int(x * nff_session.agent_histogram_frequency / nff_session.output_frequency), range(0, int((nff_session.iterations-nff_session.burn_in_its) / nff_session.agent_histogram_frequency))):
                    folder = nff_session.plot_folder + "/HISTOGRAM/AGENT/INDIVIDUAL/" + e + "/AGG/" + agent + "/" + var + "/"
                    utils.create_folder(folder)

                    if plot:
                        save_as_png = (folder + str(t * nff_session.output_frequency))
                    else:
                        save_as_png = False
                    if csv:
                        save_as_csv = (folder + str(t * nff_session.output_frequency))
                    else:
                        save_as_csv = False

                    try:
                        nff_session.generate_agent_histogram_plot(agent, var, [e], nff_session.single_ids, [t], save_as_png=save_as_png, save_as_csv=save_as_csv)
                    except:
                        print("  ERROR: ", agent, var, e, t)
    print(" DONE")


def generate_agent_histograms_aggregated_combined(nff_session, csv=True, plot=True):
    print("Generating aggregated combined agent histograms...", flush=True)
    for agent in nff_session.agent_histogram:
        for var in nff_session.agent_histogram[agent]:
            print("  " + agent + "." + var, flush=True)
            for t in map(lambda x: int(x * nff_session.agent_histogram_frequency / nff_session.output_frequency), range(0, int((nff_session.iterations-nff_session.burn_in_its) / nff_session.agent_histogram_frequency))):
                folder = nff_session.plot_folder + "/HISTOGRAM/AGENT/COMBINED/AGG/" + agent + "/" + var + "/"
                utils.create_folder(folder)

                if plot:
                    save_as_png = (folder + str(t * nff_session.output_frequency))
                else:
                    save_as_png = False
                if csv:
                    save_as_csv = (folder + str(t * nff_session.output_frequency))
                else:
                    save_as_csv = False

                try:
                    nff_session.generate_agent_histogram_plot(agent, var, nff_session.experiments, nff_session.single_ids, [t], save_as_png=save_as_png, save_as_csv=save_as_csv)
                except:
                    print("  ERROR: ", agent, var, t)
    print(" DONE")


def generate_overtime_histograms_single_runs(nff_session, csv=True, plot=True):
    print("Generating single run overtime histograms...", flush=True)
    for agent in nff_session.overtime_histogram:
        for var in nff_session.overtime_histogram[agent]:
            print("  " + agent + "." + var, flush=True)
            for e in nff_session.experiments:
                for id in nff_session.single_ids:
                    folder = nff_session.plot_folder + "/HISTOGRAM/OVER_TIME/INDIVIDUAL/" + e + "/" + str(id) + "/" + agent + "/"
                    utils.create_folder(folder)

                    if plot:
                        save_as_png = (folder + var)
                    else:
                        save_as_png = False
                    if csv:
                        save_as_csv = (folder + var)
                    else:
                        save_as_csv = False

                    try:
                        nff_session.generate_overtime_histogram_plot(agent, var, [e], [id], save_as_png=save_as_png, save_as_csv=save_as_csv)
                    except:
                        print("  ERROR: ", agent, var, e, id)
    print(" DONE")


def generate_overtime_histograms_single_runs_combined(nff_session, csv=True, plot=True):
    print("Generating single run overtime histograms combined...", flush=True)
    for agent in nff_session.overtime_histogram:
        for var in nff_session.overtime_histogram[agent]:
            print("  " + agent + "." + var, flush=True)
            for id in nff_session.single_ids:
                folder = nff_session.plot_folder + "/HISTOGRAM/OVER_TIME/COMBINED/" + str(id) + "/" + agent + "/"
                utils.create_folder(folder)

                if plot:
                    save_as_png = (folder + var)
                else:
                    save_as_png = False
                if csv:
                    save_as_csv = (folder + var)
                else:
                    save_as_csv = False

                try:
                    nff_session.generate_overtime_histogram_plot(agent, var, nff_session.experiments, [id], save_as_png=save_as_png, save_as_csv=save_as_csv)
                except:
                    print("  ERROR: ", agent, var, id)
    print(" DONE")


def generate_overtime_histograms_aggregated(nff_session, csv=True, plot=True):
    print("Generating aggregated overtime histograms...", flush=True)
    for agent in nff_session.overtime_histogram:
        for var in nff_session.overtime_histogram[agent]:
            print("  " + agent + "." + var, flush=True)
            for e in nff_session.experiments:
                folder = nff_session.plot_folder + "/HISTOGRAM/OVER_TIME/INDIVIDUAL/" + e + "/AGG/" + agent + "/"
                utils.create_folder(folder)

                if plot:
                    save_as_png = (folder + var)
                else:
                    save_as_png = False
                if csv:
                    save_as_csv = (folder + var)
                else:
                    save_as_csv = False

                try:
                    nff_session.generate_overtime_histogram_plot(agent, var, [e], nff_session.single_ids, save_as_png=save_as_png, save_as_csv=save_as_csv)
                except:
                    print("  ERROR: ", agent, var, e)
    print(" DONE")


def generate_overtime_histograms_aggregated_combined(nff_session, csv=True, plot=True):
    print("Generating aggregated overtime histograms...", flush=True)
    for agent in nff_session.overtime_histogram:
        for var in nff_session.overtime_histogram[agent]:
            print("  " + agent + "." + var, flush=True)
            folder = nff_session.plot_folder + "/HISTOGRAM/OVER_TIME/COMBINED/AGG/" + agent + "/"
            utils.create_folder(folder)

            if plot:
                save_as_png = (folder + var)
            else:
                save_as_png = False
            if csv:
                save_as_csv = (folder + var)
            else:
                save_as_csv = False
            try:
                nff_session.generate_overtime_histogram_plot(agent, var, nff_session.experiments, nff_session.single_ids, save_as_png=save_as_png, save_as_csv=save_as_csv)
            except:
                print("  ERROR: ", agent, var)

    print(" DONE")


def generate_single_run_correlation_tables(nff_session, csv=True, txt=True):
    print("Generating single run correlation tables...", flush=True)
    for corr in nff_session.correlation_table:
        print("  " + corr, flush=True)
        for e in nff_session.experiments:
            for id in nff_session.single_ids:
                folder = nff_session.table_folder + "/CORRELATIONS/INDIVIDUAL/" + e + "/" + str(id) + "/"
                utils.create_folder(folder)

                if txt:
                    save_as_txt = (folder + corr)
                else:
                    save_as_txt = False
                if csv:
                    save_as_csv = (folder + corr)
                else:
                    save_as_csv = False
                try:
                    nff_session.generate_correlation_table(nff_session.correlation_table[corr], [e], [id], save_as_csv=save_as_csv, save_as_txt=save_as_txt)
                except:
                    print("  ERROR:", corr, e, id)
    print(" DONE")


def generate_mean_correlation_tables(nff_session, csv=True, txt=True):
    print("Generating mean correlation tables...", flush=True)
    for corr in nff_session.correlation_table:
        print("  " + corr, flush=True)
        for e in nff_session.experiments:
            folder = nff_session.table_folder + "/CORRELATIONS/INDIVIDUAL/" + e + "/MEAN/"
            utils.create_folder(folder)

            if txt:
                save_as_txt = (folder + corr)
            else:
                save_as_txt = False
            if csv:
                save_as_csv = (folder + corr)
            else:
                save_as_csv = False

            try:
                nff_session.generate_correlation_table(nff_session.correlation_table[corr], [e], nff_session.single_ids, save_as_csv=save_as_csv, save_as_txt=save_as_txt)
            except:
                print("  ERROR:", corr, e)
    print(" DONE")


def generate_single_run_correlation_tables_combined(nff_session, csv=True, txt=True):
    print("Generating combined single run correlation tables...", flush=True)
    for corr in nff_session.correlation_table:
        print("  " + corr, flush=True)
        for id in nff_session.single_ids:
            folder = nff_session.table_folder + "/CORRELATIONS/COMBINED/" + str(id) + "/"
            utils.create_folder(folder)

            if txt:
                save_as_txt = (folder + corr)
            else:
                save_as_txt = False
            if csv:
                save_as_csv = (folder + corr)
            else:
                save_as_csv = False

            try:
                nff_session.generate_correlation_table(nff_session.correlation_table[corr], nff_session.experiments, [id], save_as_csv=save_as_csv, save_as_txt=save_as_txt)
            except:
                print("  ERROR:", corr, id)
    print(" DONE")


def generate_mean_correlation_tables_combined(nff_session, csv=True, txt=True):
    print("Generating combined single run correlation tables...", flush=True)
    for corr in nff_session.correlation_table:
        print("  " + corr, flush=True)
        folder = nff_session.table_folder + "/CORRELATIONS/COMBINED/MEAN/"
        utils.create_folder(folder)

        if txt:
            save_as_txt = (folder + corr)
        else:
            save_as_txt = False
        if csv:
            save_as_csv = (folder + corr)
        else:
            save_as_csv = False

        try:
            nff_session.generate_correlation_table(nff_session.correlation_table[corr],  nff_session.experiments, nff_session.single_ids, save_as_csv=save_as_csv, save_as_txt=save_as_txt)
        except:
            print("  ERROR:", corr)
    print(" DONE")


def generate_correlation_barcharts(nff_session):
    print("Generating correlation bar charts...", flush=True)
    for corr in nff_session.correlation_table:
        print("  " + corr, flush=True)
        for corr_pair in nff_session.correlation_table[corr]:
            for e in nff_session.experiments:
                folder = nff_session.table_folder + "/CORRELATIONS/INDIVIDUAL/" + e + "/BARCHART/" + corr + "/"
                utils.create_folder(folder)
                try:
                    nff_session.generate_correlation_barchart(corr_pair, [e], nff_session.single_ids, save_as_png=(folder + utils.get_label_from_corr_pair(corr_pair)))
                except:
                    print("  ERROR:", str(corr_pair))
    print(" DONE")


def generate_correlation_barcharts_combined(nff_session):
    print("Generating combined correlation bar charts...", flush=True)
    for corr in nff_session.correlation_table:
        print("  " + corr, flush=True)
        for corr_pair in nff_session.correlation_table[corr]:
            folder = nff_session.table_folder + "/CORRELATIONS/COMBINED/BARCHART/" + corr + "/"
            utils.create_folder(folder)
            try:
                nff_session.generate_correlation_barchart(corr_pair, nff_session.experiments, nff_session.single_ids, save_as_png=(folder + utils.get_label_from_corr_pair(corr_pair)))
            except:
                print("  ERROR:", corr, corr_pair)
    print(" DONE")
