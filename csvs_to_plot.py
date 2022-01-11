import os
import subprocess

# csvs is a ____ of csv files
def csvs_to_plot(plot_target_directory, figure, gryff_csv, gus_csv, epaxos_csv, is_for_reads, log=False):

    plot_script_file = os.path.join(plot_target_directory, '%s.gpi' % figure)

    csvs = (gryff_csv, gus_csv, epaxos_csv)
    protocols = ["Gryff", "Gus", "EPaxos"]  # should match with csvs passed in
    generate_gnuplot_script(plot_script_file, plot_target_directory, csvs, protocols, is_for_reads=is_for_reads, log=log)

    subprocess.call(['gnuplot', plot_script_file])

# TODO: This is important
def generate_gnuplot_script(plot_script_file, plot_target_directory, csvs, protocols, is_for_reads, log=False):
    with open(plot_script_file, 'w+') as f:
        f.write("set datafile separator ','\n")

        f.write("set key bottom right\n")
        f.write("set xlabel 'Latency (ms)'\n")

        if is_for_reads:
            f.write("set ylabel 'Fraction of Reads'\n")
        else:
            f.write("set ylabel 'Fraction of Writes'\n")

        f.write("set terminal pngcairo size 800,600 enhanced font 'DejaVu Sans,12'\n") # TODO increase font size, this doesn't work
        f.write('set output \'%s/%s\'\n' % (plot_target_directory, os.path.splitext(os.path.basename(plot_script_file))[0] + '.png'))

        f.write('set style line 1 linetype 1 linecolor "green" linewidth 3 dashtype 2\n')
        f.write('set style line 2 linetype 1 linecolor "orange" linewidth 3 dashtype 1\n')
        f.write('set style line 3 linetype 1 linecolor "blue" linewidth 3 dashtype 3\n')

        f.write('plot ')
        for i in range(len(csvs)):
            if log:
                f.write("'%s' using 1:(-log10(1-$2)):yticlabels(3) title '%s' ls %d with lines" % (csvs[i], protocols[i], i + 1))
            else:
                f.write("'%s' title '%s' ls %d with lines" % (csvs[i], protocols[i], i + 1))
            if i != len(csvs) - 1:
                f.write(', \\\n')