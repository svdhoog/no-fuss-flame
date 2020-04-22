import argparse
from pyflame import auto
from pyflame import FlameSession
import multiprocessing

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Basic tool to configure and execute experiments for Flame models')
    parser.add_argument("config", help="configuration file")
    parser.add_argument("-n", "--cpus", action="store", type=int, help="Number of cpus used")
    parser.add_argument("--skip", help="Skip existing runs", action="store_true")
    parser.add_argument("--dont_build", help="Do not compile and parse the model", action="store_true")
    parser.add_argument("--dont_run", help="Do not run the simulation", action="store_true")
    parser.add_argument("--no_plots", help="Do not create plots", action="store_true")
    parser.add_argument("--no_csv", help="Do not create csv files", action="store_true")
    parser.add_argument("--no_txt", help="Do not create text files", action="store_true")
    parser.add_argument("--no_results", help="Do not provide any results", action="store_true")
    parser.add_argument("--only_combined", help="only provide combined results", action="store_true")
    parser.add_argument("--only_aggregated", help="only provide aggregated results", action="store_true")

    args = parser.parse_args()

    session = FlameSession(args.config)

    csv = not args.no_csv
    plot = not args.no_plots
    txt = not args.no_txt

    if args.cpus is not None:
        cpus = args.cpus
    else:
        cpus = multiprocessing.cpu_count()

    if not (args.dont_build or args.dont_run):
        session.parse_model()
        session.compile_model()
    if not args.dont_run:
        session.simulate_model_transient(cpus, skip=args.skip)

    if not (args.dont_build or args.dont_run):
        session.modify_xml()
        session.compile_model()

    if not args.dont_run:
        session.simulate_model(cpus, skip=args.skip)

    if not args.no_results:
        if args.dont_run and session.cache_file_exists():
            session.load_data_from_cache()
        else:
            session.load_simulated_data()
            session.write_data_to_cache()

        if not args.only_aggregated:
            if not args.only_combined:
                auto.generate_single_run_time_series_plots(session, csv=csv, plot=plot)
                auto.generate_single_agent_time_series_plots(session, csv=csv, plot=plot)
                auto.generate_agent_histograms_single_runs(session, csv=csv, plot=plot)
                auto.generate_overtime_histograms_single_runs(session, csv=csv, plot=plot)
                auto.generate_single_run_correlation_tables(session, csv=csv, txt=txt)
                auto.generate_mean_correlation_tables(session, csv=csv, txt=txt)

            if len(session.experiments) > 1:
                auto.generate_single_run_time_series_plots_combined(session, csv=csv, plot=plot)
                auto.generate_single_agent_time_series_plots_combined(session, csv=csv, plot=plot)
                auto.generate_agent_histograms_single_runs_combined(session, csv=csv, plot=plot)
                auto.generate_overtime_histograms_single_runs_combined(session, csv=csv, plot=plot)
                auto.generate_single_run_correlation_tables_combined(session, csv=csv, txt=txt)

        if not args.only_combined:
            auto.generate_aggregated_time_series_plots(session, csv=csv, plot=plot)
            auto.generate_agent_histograms_aggregated(session, csv=csv, plot=plot)
            auto.generate_overtime_histograms_aggregated(session, csv=csv, plot=plot)
            auto.generate_all_runs_time_series_plots(session, csv=csv, plot=plot)
            auto.generate_correlation_barcharts(session)

        if len(session.experiments) > 1:
            auto.generate_all_runs_time_series_plots_combined(session, csv=csv, plot=plot)
            auto.generate_aggregated_time_series_plots_combined(session, csv=csv, plot=plot)
            auto.generate_agent_histograms_aggregated_combined(session, csv=csv, plot=plot)
            auto.generate_overtime_histograms_aggregated_combined(session, csv=csv, plot=plot)
            auto.generate_all_runs_time_series_plots_combined(session, csv=csv, plot=plot)
            auto.generate_mean_correlation_tables_combined(session, csv=csv, txt=txt)
            auto.generate_correlation_barcharts_combined(session)
