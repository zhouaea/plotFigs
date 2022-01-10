import glob

# This is a hack to get gus data to plot with gryff and multipaxos data derived from gryff repo.
import os.path

def main():
    # test stuff
    plot_figs()

# Supply paths to gryff csv files, epaxos latency files, gus latency files.
def plot_figs(gryff_6a_norm_cdf_csv, gryff_6a_norm_log_cdf_csv,
              gryff_6b_norm_cdf_csv, gryff_6b_norm_log_cdf_csv,
              gryff_6c_norm_cdf_csv, gryff_6c_norm_log_cdf_csv,
              gryff_8a_norm_cdf_csv, gryff_8b_norm_cdf_csv,
              gryff_9a_norm_cdf_csv,gryff_9b_norm_cdf_csv,
              gus_6a_latency_folder, gus_6b_latency_folder, gus_8_latency_folder, gus_9_latency_folder,
              epaxos_6a_latency_folder, epaxos_6b_latency_folder, epaxos_8_latency_folder, epaxos_9_latency_folder):

    # TODO plot config file
    plot_config = None

    gryff_fig_6_csvs = (gryff_6a_norm_cdf_csv, gryff_6a_norm_log_cdf_csv,
                        gryff_6b_norm_cdf_csv, gryff_6b_norm_log_cdf_csv,
                        gryff_6c_norm_cdf_csv, gryff_6c_norm_log_cdf_csv)
    plot_fig_6(plot_config, gryff_fig_6_csvs, gus_6a_latency_folder, gus_6b_latency_folder, epaxos_6a_latency_folder, epaxos_6b_latency_folder)

    # gryff_fig_8_csvs = (gryff_8a_norm_cdf_csv, gryff_8b_norm_cdf_csv)
    # plot_fig_8(plot_config, gryff_fig_8_csvs, gus_8_latency_folder, epaxos_8_latency_folder)
    #
    # gryff_fig_9_csvs = (gryff_9a_norm_cdf_csv,gryff_9b_norm_cdf_csv)
    # plot_fig_9(plot_config, gryff_fig_9_csvs, gus_9_latency_folder, epaxos_9_latency_folder)

# 2%, 10%, 25% conflicts, only plot read data
def plot_fig_6(plot_config,
               gryff_fig_6_csvs,
               gus_6a_latency_folder, gus_6b_latency_folder,
               epaxos_6a_latency_folder, epaxos_6b_latency_folder):

    gus_fig_6_csvs, epaxos_fig_6_csvs = calculate_fig_6_csvs()


def calculate_fig_6_csvs(gus_6a_latency_folder, gus_6b_latency_folder,
                         epaxos_6a_latency_folder, epaxos_6b_latency_folder):
    # Combine data in each latency folder. We only need reads, no writes.
    gus_6a_reads, _ = extract_latencies(gus_6a_latency_folder)
    gus_6b_reads, _ = extract_latencies(gus_6b_latency_folder)
    epaxos_6a_reads, _ = extract_latencies(epaxos_6a_latency_folder)
    epaxos_6b_reads, _ = extract_latencies(epaxos_6b_latency_folder)

    # Calculate csvs for each combined datum.


    # Package csvs into tuples before returning them
    gus_fig_6_csvs = (gus_6a_norm_cdf_csv, gus_6a_norm_log_cdf_csv,
                      gus_6b_norm_cdf_csv, gus_6b_norm_log_cdf_csv)
    epaxos_fig_6_csvs = (epaxos_6a_norm_cdf_csv, epaxos_6a_norm_log_cdf_csv,
                        epaxos_6b_norm_cdf_csv, epaxos_6b_norm_log_cdf_csv)
    return gus_fig_6_csvs, epaxos_fig_6_csvs

def extract_latencies(folder):
    reads = []
    writes = []

    read_files = glob.glob(os.path.join(folder, "latFileRead*"))
    write_files = glob.glob(os.path.join(folder, "latFileWrite*"))

    i = 0

    for read_file in read_files:
        i += 1
        with open(read_file) as f:
            ops = f.readlines()
            print("len of %dth file is %d" % (i, len(ops)))
            for op in ops:
                reads.append(op[1])

    for write_file in write_files:
        i += 1
        with open(write_file) as f:
            ops = f.readlines()
            print("len of %dth file is %d" % (i, len(ops)))
            for op in ops:
                writes.append(op[1])

    print("First five read and write latencies:")
    print(reads[:5], writes[:5])

    return reads, writes

# # 49.5 reads, 49.5% writes, and 1.0% rmws with 25% conflicts, plot read and write data n = 3
# def plot_fig_8(plot_config, gryff_8_norm_cdf_csv, gus_8_latency_folder, epaxos_8_latency_folder):
#
# # 49.5 reads, 49.5% writes, and 1.0% rmws with 25% conflicts, plot read and write data. n = 5
# def plot_fig_9(plot_config, gryff_9_norm_cdf_csv, gus_9_latency_folder, epaxos_9_latency_folder):

