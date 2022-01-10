import os
import subprocess

# csvs is a ____ of csv files
def csvs_to_plot(plot_name, plots_directory, plot_config, gryff_csv, gus_csv, epaxos_csv, log=False):
    # plot all protocols on one graph
    if log:
        plot_script_file = os.path.join(plots_directory, '%s.gpi' % plot_name)
        generate_gnuplot_script_cdf(plot_config, plot_script_file)
        run_gnuplot([gryff_csv, gus_csv, epaxos_csv], os.path.join(plots_directory, '%s.png' % plot_name),
            plot_script_file)
    else:
        plot_script_file = os.path.join(plots_directory, '%s-log.gpi' % plot_name)
        generate_gnuplot_script_cdf_log(plot_config, plot_script_file)
        run_gnuplot([gryff_csv, gus_csv, epaxos_csv], os.path.join(plots_directory, '%s.png' % plot_name),
            plot_script_file)

# TODO: This is important
def generate_gnuplot_script_agg(plot, plot_script_file, plot_out_file, series):
    with open(plot_script_file, 'w') as f:
        write_gpi_header(f)
        f.write("set key top left\n")
        f.write("set xlabel '%s'\n" % config['plot_cdf_x_label'])
        f.write("set ylabel '%s'\n" % config['plot_cdf_y_label'])
        f.write("set terminal pngcairo size %d,%d enhanced font '%s'\n" %
                (config['plot_cdf_png_width'], config['plot_cdf_png_height'],
                 config['plot_cdf_png_font']))
        f.write('set output \'%s\'\n' % plot_out_file)
        write_line_styles(f)
        f.write('plot ')
        for i in range(len(series)):
            f.write("'%s' title '%s' ls %d with linespoint" % (series[i], plot['series_titles'][i].replace('_', '\\_'), i + 1))
            if i != len(series) - 1:
                f.write(', \\\n')

def generate_gnuplot_script_cdf(config, script_file):
    with open(script_file, 'w') as f:
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
    with open(script_file, 'w') as f:
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