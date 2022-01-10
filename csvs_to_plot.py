import os
import subprocess

# csvs is a ____ of csv files
def csvs_to_plot(plot_target_directory, figure, gryff_csv, gus_csv, epaxos_csv, is_for_reads, log=False):

    if log:
        plot_script_file = os.path.join(plot_target_directory, '%s.gpi' % figure)
    else:
        plot_script_file = os.path.join(plot_target_directory, '%s-log.gpi' % figure)

    csvs = (gryff_csv, gus_csv, epaxos_csv)
    protocols = ["Gryff", "Gus", "EPaxos"]  # should match with csvs passed in
    generate_gnuplot_script(plot_script_file, plot_target_directory, csvs, protocols, is_for_reads=is_for_reads, log=log)

    run_gnuplot(csvs, os.path.join(plot_target_directory, '%s.png' % figure), plot_script_file)

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

        f.write("set terminal pngcairo size 600,800 enhanced font 'DejaVu Sans,12'\n")
        f.write('set output \'%s\'\n' % plot_target_directory)

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

def generate_gnuplot_script_cdf(config, script_file):
    with open(script_file, 'w+') as f:
        f.write("set datafile separator ','\n")
        f.write("set key bottom right\n")
        f.write("set xlabel '%s'\n" % config['plot_cdf_x_label'])
        f.write("set ylabel '%s'\n" % config['plot_cdf_y_label'])
        f.write("set terminal pngcairo size %d,%d enhanced font '%s'\n" %
                (config['plot_cdf_png_width'], config['plot_cdf_png_height'],
                 config['plot_cdf_png_font']))
        f.write('set output outfile\n')
        f.write("plot datafile0 title '%s' with lines\n" % config['plot_cdf_series_title'].replace('_', '\\_'))

def generate_gnuplot_script_cdf_log(config, script_file):
    with open(script_file, 'w+') as f:
        f.write("set datafile separator ','\n")
        f.write("set key bottom right\n")
        f.write("set xlabel '%s'\n" % config['plot_cdf_x_label'])
        f.write("set ylabel '%s'\n" % config['plot_cdf_y_label'])
        f.write("set terminal pngcairo size %d,%d enhanced font '%s'\n" %
                (config['plot_cdf_png_width'], config['plot_cdf_png_height'],
                 config['plot_cdf_png_font']))
        f.write('set output outfile\n')
        f.write("plot datafile0 using 1:(-log10(1-$2)):yticlabels(3) title '%s' with lines\n" % config['plot_cdf_series_title'].replace('_', '\\_'))

def run_gnuplot(data_files, out_file, script_file):
    print(script_file)
    args = ['gnuplot', '-e', "outfile='%s'" % out_file]
    for i in range(len(data_files)):
        args += ['-e', "datafile%d='%s'" % (i, data_files[i])]
    args.append(script_file)
    subprocess.call(args)