#! /usr/bin/env python

# Copyright (C) 2018  Charlie Hoy <charlie.hoy@ligo.org>
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import pesummary
from pesummary.core.plots import plot as core
from pesummary.gw.plots import plot as gw
from pesummary.gw.plots import publication as pub
from pesummary.gw.plots.latex_labels import GWlatex_labels
from pesummary.core.plots.latex_labels import latex_labels
from pesummary.core.file.read import read as Read
from pesummary.gw.file.read import read as GWRead
from pesummary.utils.utils import logger, resample_posterior_distribution
from pesummary.core.command_line import command_line
from pesummary.core.inputs import Input
from pesummary.gw.inputs import GWInput
from pesummary.gw.command_line import insert_gwspecific_option_group
from pesummary.utils import functions

import warnings
import multiprocessing as mp

from glob import glob
import math
import numpy as np

try:
    import ligo.skymap
    SKYMAP = True
except ImportError:
    SKYMAP = False


__doc__ == "Class to generate plots"


latex_labels.update(GWlatex_labels)


class PlotGeneration(pesummary.core.inputs.PostProcessing):
    """Class to generate all available plots for each results file.

    Parameters
    ----------
    parser: argparser
        The parser containing the command line arguments

    Attributes
    ----------
    savedir: str
        The path to the directory where all plots will be saved
    """
    def __init__(self, inputs, colors="default"):
        super(PlotGeneration, self).__init__(inputs, colors)
        self.inputs = inputs
        logger.info("Starting to generate plots")
        self.generate_plots()
        logger.info("Finished generating the plots")

    @staticmethod
    def _check_latex_labels(parameters):
        for i in parameters:
            if i not in list(latex_labels.keys()):
                latex_labels[i] = i.replace("_", " ")

    @property
    def savedir(self):
        return self.webdir + "/plots/"

    def generate_plots(self):
        """Generate all plots for all results files.
        """
        for i in self.labels:
            logger.debug("Starting to generate plots for %s\n" % (i))
            self._check_latex_labels(self.samples[i].keys())
            self.try_to_make_a_plot("corner", i)
            self.try_to_make_a_plot("1d_histogram", i)
            if self.custom_plotting:
                self.try_to_make_a_plot("custom", num)
        if self.add_to_existing:
            existing = Read(self.existing_meta_file)
            existing_config = glob(self.existing + "/config/*")
            for num, i in enumerate(existing.labels):
                original_label = existing.labels[num]
                self.labels.append(original_label)
                self.result_files.append(self.existing)
                self.samples.append(existing.samples[num])
                self.parameters.append(existing.parameters[num])
                if self.config and len(existing_config) >= 1:
                    self.config.append(existing_config[num])
                self.injection_data.append(existing.injection_parameters[num])
                self.file_versions.append(existing.input_version[num])
                self.file_kwargs.append(existing.extra_kwargs[num])
            self.same_parameters = list(
                set.intersection(*[set(l) for l in self.parameters]))
        if len(self.samples) > 1:
            logger.debug("Starting to generate comparison plots\n")
            self.try_to_make_a_plot("1d_histogram_comparison", "all")
            if self.custom_plotting:
                self.try_to_make_a_plot("custom", "all")

    def try_to_make_a_plot(self, plot_type, label=None):
        """Try and make a plot. If it fails, return an error.

        Parameters
        ----------
        plot_type: str
            String for the plot that you wish to try and make
        idx: int
            The index of the results file that you wish to analyse.
        """
        plot_type_dictionary = {"corner": self._corner_plot,
                                "1d_histogram": self._1d_histogram_plots,
                                "1d_histogram_comparison":
                                self._1d_histogram_comparison_plots,
                                "custom": self._custom_plots}
        try:
            plot_type_dictionary[plot_type](label)
        except Exception as e:
            logger.info("Failed to generate %s plot because "
                        "%s" % (plot_type, e))
            plt.close()

    def _corner_plot(self, label):
        """Generate a corner plot for a given results file.

        Parameters
        ----------
        idx: int
            The index of the results file that you wish to analyse
        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fig, params = core._make_corner_plot(
                self.samples[label], list(self.samples[label].keys()), latex_labels
            )
            plt.savefig("%s/corner/%s_all_density_plots.png" % (
                self.savedir, label)
            )
            plt.close()
            combine_corner = open("%s/js/combine_corner.js" % (self.webdir))
            combine_corner = combine_corner.readlines()
            params = [str(i) for i in params]
            ind = [linenumber for linenumber, line in enumerate(combine_corner)
                   if "var list = {}" in line][0]
            combine_corner.insert(
                ind + 1, "    list['%s'] = %s;\n" % (label, params)
            )
            new_file = open("%s/js/combine_corner.js" % (self.webdir), "w")
            new_file.writelines(combine_corner)
            new_file.close()

    def _1d_histogram_plots(self, label):
        """Generate 1d_histogram plots, sample evolution plots, plots
        showing the autocorrelation function and the CDF plots for all
        parameters in the results file.

        Parameters
        ----------
        idx: int
            The index of the results file that you wish to analyse
        """
        for ind, j in enumerate(self.samples[label].keys()):
            try:
                inj_value = self.injection_data[label][j]
                if math.isnan(inj_value):
                    inj_value = None
                fig = core._1d_histogram_plot(
                    j, self.samples[label][j], latex_labels[j], inj_value,
                    kde=self.kde_plot)
                plt.savefig(self.savedir + "%s_1d_posterior_%s.png" % (
                    label, j)
                )
                plt.close()
                fig = core._sample_evolution_plot(
                    j, self.samples[label][j], latex_labels[j], inj_value
                )
                plt.savefig(self.savedir + "%s_sample_evolution_%s.png" % (
                    label, j)
                )
                plt.close()
                fig = core._autocorrelation_plot(j, self.samples[label][j])
                plt.savefig(self.savedir + "%s_autocorrelation_%s.png" % (
                    label, j))
                plt.close()
                fig = core._1d_cdf_plot(j, self.samples[label][j], latex_labels[j])
                fig.savefig(self.savedir + "%s_cdf_%s.png" % (
                    label, j))
                plt.close()
            except Exception as e:
                logger.info("Failed to generate 1d_histogram plots for %s "
                            "because %s" % (j, e))
                plt.close()
                continue

    def _1d_histogram_comparison_plots(self, idx="all"):
        """Generate comparison plots for all parameters that are consistent
        across all results files.

        Parameters
        ----------
        idx: int, optional
            The indicies of the results files that you wish to be included
            in the comparsion plots.
        """
        for ind, j in enumerate(self.same_parameters):
            try:
                indices = [k.index("%s" % (j)) for k in self.parameters]
                param_samples = [[k[indices[num]] for k in l] for num, l in
                                 enumerate(self.samples)]
                fig = core._1d_comparison_histogram_plot(
                    j, param_samples, self.colors,
                    latex_labels[j], self.labels, kde=self.kde_plot)
                plt.savefig(self.savedir + "combined_1d_posterior_%s" % (j))
                plt.close()
                fig = core._1d_cdf_comparison_plot(
                    j, param_samples, self.colors,
                    latex_labels[j], self.labels)
                fig.savefig(self.savedir + "combined_cdf_%s" % (j))
                plt.close()
                fig = core._comparison_box_plot(
                    j, param_samples, self.colors, latex_labels[j],
                    self.labels)
                fig.savefig(self.savedir + "combined_boxplot_%s" % (j))
                plt.close()
            except Exception as e:
                logger.info("Failed to generate comparison plots for %s "
                            "because %s" % (j, e))
                plt.close()
                continue

    def _custom_plots(self, idx="all"):
        """Generate custom plots according to the passed python file

        Parameters
        ----------
        idx: int
            The index of the results file that you wish to analyse
        """
        import importlib

        if self.custom_plotting[0] != "":
            import sys

            sys.path.append(self.custom_plotting[0])
        mod = importlib.import_module(self.custom_plotting[1])

        if idx != "all":
            methods = [getattr(mod, i) for i in mod.__single_plots__]

            for num, i in enumerate(methods):
                fig = i(self.parameters[idx], self.samples[idx])
                fig.savefig(self.savedir + "%s_custom_plotting_%s" % (
                    self.labels[idx], num))
                plt.close()
        else:
            methods = [getattr(mod, i) for i in mod.__comparison_plots__]

            for num, i in enumerate(methods):
                fig = i(self.parameters, self.samples, self.labels)
                fig.savefig(self.savedir + "combined_custom_plotting_%s" % (num))
                plt.close()


class GWPlotGeneration(pesummary.gw.inputs.GWPostProcessing, PlotGeneration):
    """Class to generate all available plots for each results file.

    Parameters
    ----------
    parser: argparser
        The parser containing the command line arguments

    Attributes
    ----------
    savedir: str
        The path to the directory where all plots will be saved
    """
    def __init__(self, inputs, colors="default"):
        super(GWPlotGeneration, self).__init__(inputs, colors)
        self.inputs = inputs
        logger.info("Starting to generate plots")
        self.generate_plots()
        logger.info("Finished generating the plots")

    def generate_plots(self):
        """Generate all plots for all results files.
        """
        if self.calibration_samples or self.calibration_prior:
            logger.debug("Generating the calibration plot")
            for num, i in enumerate(self.result_files):
                self.try_to_make_a_plot("calibration", num)
        if self.psds:
            logger.debug("Generating the psd plot")
            for num, i in enumerate(self.result_files):
                self.try_to_make_a_plot("psd", num)
        for num, i in enumerate(self.result_files):
            logger.debug("Starting to generate plots for %s\n" % (i))
            self._check_latex_labels(self.parameters[num])
            self.try_to_make_a_plot("corner", num)
            self.try_to_make_a_plot("skymap", num)
            self.try_to_make_a_plot("waveform", num)
            if self.gwdata:
                self.try_to_make_a_plot("data", num)
            self.try_to_make_a_plot("1d_histogram", num)
            if self.custom_plotting:
                self.try_to_make_a_plot("custom", num)
            self.try_to_make_a_plot("pepredicates", num)
        if self.sensitivity:
            self.try_to_make_a_plot("sensitivity", 0)
        if self.add_to_existing:
            existing = GWRead(self.existing_meta_file)
            existing_config = glob(self.existing + "/config/*")
            for num, i in enumerate(existing.labels):
                original_label = existing.labels[num]
                self.labels.append(original_label)
                self.result_files.append(self.existing)
                self.samples.append(existing.samples[num])
                self.parameters.append(existing.parameters[num])
                if existing.approximant[num]:
                    self.approximant.append(existing.approximant[num])
                else:
                    self.approximant.append(None)
                if self.config and len(existing_config) > 1:
                    self.config.append(existing_config[num])
                self.injection_data.append(existing.injection_parameters[num])
                self.file_versions.append(existing.input_version[num])
                self.file_kwargs.append(existing.extra_kwargs[num])
            key_data = self._key_data()
            maxL_list = []
            for idx, j in enumerate(self.parameters):
                dictionary = {k: key_data[idx][k]["maxL"] for k in j}
                maxL_list.append(dictionary)
            self.maxL_samples = maxL_list
            self.same_parameters = list(
                set.intersection(*[set(l) for l in self.parameters]))
        if len(self.samples) > 1:
            logger.debug("Starting to generate comparison plots\n")
            self.try_to_make_a_plot("1d_histogram_comparison", "all")
            self.try_to_make_a_plot("skymap_comparison", "all")
            self.try_to_make_a_plot("waveform_comparison", "all")
            if self.publication:
                self.try_to_make_a_plot("2d_comparison_contour_plots", "all")
                self.try_to_make_a_plot("violin_plots", "all")
                self.try_to_make_a_plot("spin_disk_plots", "all")

    def try_to_make_a_plot(self, plot_type, idx=None):
        """Try and make a plot. If it fails, return an error.

        Parameters
        ----------
        plot_type: str
            String for the plot that you wish to try and make
        idx: int
            The index of the results file that you wish to analyse.
        """
        plot_type_dictionary = {"calibration": self._calibration_plot,
                                "psd": self._psd_plot,
                                "corner": self._corner_plot,
                                "skymap": self._skymap_plot,
                                "waveform": self._waveform_plot,
                                "data": self._strain_plot,
                                "1d_histogram": self._1d_histogram_plots,
                                "1d_histogram_comparison":
                                self._1d_histogram_comparison_plots,
                                "skymap_comparison":
                                self._skymap_comparison_plot,
                                "waveform_comparison":
                                self._waveform_comparison_plot,
                                "sensitivity": self._sensitivity_plot,
                                "custom": self._custom_plots,
                                "2d_comparison_contour_plots":
                                self._2d_comparison_contour_plots,
                                "violin_plots": self._violin_plots,
                                "spin_disk_plots": self._spin_disk_plots,
                                "pepredicates": self._pepredicates_plot}
        try:
            plot_type_dictionary[plot_type](idx)
        except Exception as e:
            logger.info("Failed to generate %s plot because "
                        "%s" % (plot_type, e))
            plt.close()

    def _calibration_plot(self, idx=None):
        """Generate a single plot showing the calibration envelopes for all
        IFOs used in the analysis.
        """
        frequencies = np.arange(20., 1024., 1. / 4)
        if self.calibration_envelopes[idx] is not None:
            fig = gw._calibration_envelope_plot(
                frequencies, self.calibration_envelopes[idx],
                self.calibration_labels[idx], prior=self.calibration_prior_envelopes[idx])
            fig.savefig("%s/%s_calibration_plot.png" % (self.savedir, self.labels[idx]))
            plt.close()

    def _psd_plot(self, idx=None):
        """Generate a single plot showing all psds used in analysis
        """
        frequencies = self.psd_frequencies[idx]
        strains = self.psd_strains[idx]
        fmin = None
        if "f_low" in list(self.file_kwargs[idx]["sampler"].keys()):
            fmin = self.file_kwargs[idx]["sampler"]["f_low"]
        fig = gw._psd_plot(
            frequencies, strains, labels=self.psd_labels[idx], fmin=fmin)
        fig.savefig("%s/%s_psd_plot.png" % (self.savedir, self.labels[idx]))
        plt.close()

    def _corner_plot(self, idx):
        """Generate a corner plot for a given results file.

        Parameters
        ----------
        idx: int
            The index of the results file that you wish to analyse
        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fig, params = gw._make_corner_plot(
                self.samples[idx], self.parameters[idx], latex_labels)
            plt.savefig("%s/corner/%s_all_density_plots.png" % (
                self.savedir, self.labels[idx]))
            plt.close()
            combine_corner = open("%s/js/combine_corner.js" % (self.webdir))
            combine_corner = combine_corner.readlines()
            params = [str(i) for i in params]
            ind = [linenumber for linenumber, line in enumerate(combine_corner)
                   if "var list = {}" in line][0]
            combine_corner.insert(ind + 1, "    list['%s'] = %s;\n" % (
                self.labels[idx], params))
            new_file = open("%s/js/combine_corner.js" % (self.webdir), "w")
            new_file.writelines(combine_corner)
            new_file.close()
            fig = gw._make_source_corner_plot(
                self.samples[idx], self.parameters[idx], latex_labels)
            plt.savefig("%s/corner/%s_source_frame.png" % (
                self.savedir, self.labels[idx]))
            plt.close()
            fig = gw._make_extrinsic_corner_plot(
                self.samples[idx], self.parameters[idx], latex_labels)
            plt.savefig("%s/corner/%s_extrinsic.png" % (
                self.savedir, self.labels[idx]))
            plt.close()

    def _skymap_plot(self, idx):
        """Generate a skymap showing the confidence regions for a given results
        file.


        Parameters
        ----------
        idx: int
            The index of the results file that you wish to analyse
        """
        from pesummary.utils.utils import RedirectLogger

        ind_ra = self.parameters[idx].index("ra")
        ind_dec = self.parameters[idx].index("dec")
        ra = [j[ind_ra] for j in self.samples[idx]]
        dec = [j[ind_dec] for j in self.samples[idx]]

        fig = gw._default_skymap_plot(ra, dec)
        fig.savefig(self.savedir + "/%s_skymap.png" % (
            self.labels[idx]))
        plt.close()

        if SKYMAP and not self.no_ligo_skymap:
            logger.info("Launching subprocess to generate skymap plot with "
                        "ligo.skymap")
            try:
                with RedirectLogger("ligo.skymap", level="DEBUG") as redirector:
                    process = mp.Process(target=self._ligo_skymap_plot,
                                         args=[ra, dec, idx])
                    process.start()
            except Exception as e:
                logger.warn("Failed to generate a skymap using the ligo.skymap "
                            "package because %s. Using the default PESummary "
                            "skymap plotter instead" % (e))

    def _ligo_skymap_plot(self, ra, dec, idx):
        """Generate a skymap produced from the ligo.skymap code

        Parameters
        ----------
        ra: list
            list of samples for right ascension
        dec: list
            list of samples for declination
        idx: int
            the index of the results file that you wish to analyse
        """
        downsampled = False
        if self.nsamples_for_skymap:
            ra, dec = resample_posterior_distribution(
                [ra, dec], self.nsamples_for_skymap)
            downsampled = True
        fig = gw._ligo_skymap_plot(ra, dec, savedir=self.webdir + "/samples",
                                   nprocess=self.multi_threading_for_skymap,
                                   downsampled=downsampled)
        fig.savefig(self.savedir + "/%s_skymap.png" % (
            self.labels[idx]))
        plt.close()

    def _sensitivity_plot(self, idx):
        """Generate a plot showing the network sensitivity for the maximum
        likelihood waveform.

        Parameters
        ----------
        idx: int
            The index of the results file that you wish to analyse
        """
        fig = gw._sky_sensitivity(["H1", "L1"], 0.2, self.maxL_samples[idx])
        plt.savefig(self.savedir + "%s_sky_sensitivity_HL" % (
            self.approximant[idx]))
        plt.close()
        fig = gw._sky_sensitivity(
            ["H1", "L1", "V1"], 0.2, self.maxL_samples[idx])
        fig.savefig(self.savedir + "%s_sky_sensitivity_HLV" % (
            self.labels[idx]))
        plt.close()

    def _waveform_plot(self, idx):
        """Generate a plot showing the maximum likelihood waveform in each
        available detector.

        Parameters
        ----------
        idx: int
            The index of the results file that you wish to analyse
        """
        if self.detectors[idx] is None:
            detectors = ["H1", "L1"]
        else:
            detectors = self.detectors[idx].split("_")
        fig = gw._waveform_plot(detectors, self.maxL_samples[idx])
        plt.savefig(self.savedir + "%s_waveform.png" % (
            self.labels[idx]))
        plt.close()
        fig = gw._time_domain_waveform(detectors, self.maxL_samples[idx])
        fig.savefig(self.savedir + "%s_waveform_timedomain.png" % (
            self.labels[idx]))
        plt.close()

    def _strain_plot(self, idx):
        """Launch a subprocess to generate a the strain plot
        """
        logger.info("Launching subprocess to generate strain plot")
        try:
            process = mp.Process(target=self.__strain_plot, args=[idx])
            process.start()
        except Exception as e:
            logger.warn("Failed to generate the strain plot because %s" % (e))

    def __strain_plot(self, idx):
        """Generate a plot showing the data with the maximum likelihood
        waveform in each available detector
        """
        fig = gw._strain_plot(self.gwdata, self.maxL_samples[idx])
        plt.savefig(self.savedir + "%s_strain.png" % (self.labels[idx]))
        plt.close()

    def _skymap_comparison_plot(self, idx="all"):
        """Generate a comparison skymap plot.

        Parameters
        ----------
        idx: int, optional
            The indicies of the results files that you wish to be included
            in the comparsion plots.
        """
        ind_ra = [i.index("ra") for i in self.parameters]
        ind_dec = [i.index("dec") for i in self.parameters]
        ra_list = [[k[ind_ra[num]] for k in l] for num, l in
                   enumerate(self.samples)]
        dec_list = [[k[ind_dec[num]] for k in l] for num, l in
                    enumerate(self.samples)]
        fig = gw._sky_map_comparison_plot(
            ra_list, dec_list, self.labels, self.colors)
        fig.savefig(self.savedir + "combined_skymap.png")
        plt.close()

    def _waveform_comparison_plot(self, idx="all"):
        """Generate a plot to compare waveforms as seen in the Hanford
        detector.

        Parameters
        ----------
        idx: int, optional
            The indicies of the results files that you wish to be included
            in the comparsion plots.
        """
        fig = gw._waveform_comparison_plot(
            self.maxL_samples, self.colors, self.labels)
        fig.savefig(self.savedir + "compare_waveforms.png")
        plt.close()
        fig = gw._time_domain_waveform_comparison_plot(
            self.maxL_samples, self.colors, self.labels)
        fig.savefig(self.savedir + "compare_time_domain_waveforms.png")
        plt.close()

    def _2d_comparison_contour_plots(self, idx="all"):
        """Generate 2d comparison contour plots

        Parameters
        ----------
        idx: int, optional
            The indicies of the results files that you wish to be included
            in the comparsion plots.
        """
        twod_plots = [["mass_ratio", "chi_eff"], ["mass_1", "mass_2"],
                      ["luminosity_distance", "chirp_mass_source"],
                      ["mass_1_source", "mass_2_source"],
                      ["theta_jn", "luminosity_distance"],
                      ["network_optimal_snr", "chirp_mass_source"]]
        for i in twod_plots:
            if not all(all(j in k for j in i) for k in self.parameters):
                logger.warn("Failed to generate 2d comparison contour plot for "
                            "%s" % ("_and_".join(i)))
                continue
            try:
                ind1 = [j.index(i[0]) for j in self.parameters]
                ind2 = [j.index(i[1]) for j in self.parameters]
                samples1 = [[k[ind1[num]] for k in l] for num, l in
                            enumerate(self.samples)]
                samples2 = [[k[ind2[num]] for k in l] for num, l in
                            enumerate(self.samples)]
                samples = [[j, k] for j, k in zip(samples1, samples2)]
                fig = pub.twod_contour_plots(
                    i, samples, self.labels, latex_labels)
                fig.savefig("%s/publication/2d_contour_plot_%s.png" % (
                    self.savedir, "_and_".join(i)))
                plt.close()
            except Exception:
                logger.warn("Failed to generate 2d contour plot for %s" % (
                            "_and_".join(i)))
                continue

    def _violin_plots(self, idx="all"):
        """Generate 2d comparison contour plots

        Parameters
        ----------
        idx: int, optional
            The indicies of the results files that you wish to be included
            in the comparsion plots.
        """
        violin_plots = ["mass_ratio", "chi_eff", "chi_p", "luminosity_distance"]
        for i in violin_plots:
            if not all(i in j for j in self.parameters):
                logger.warn("Failed to generate violin plots for %s because "
                            "%s is not in all result files" % (i, i))
                continue
            try:
                ind = [j.index(i) for j in self.parameters]
                samples = [[k[ind[num]] for k in l] for num, l in
                           enumerate(self.samples)]
                fig = pub.violin_plots(i, samples, self.labels, latex_labels)
                fig.savefig("%s/publication/violin_plot_%s.png" % (
                    self.savedir, i))
                plt.close()
            except Exception:
                logger.warn("Failed to generate a violin plot for %s" % (i))
                continue

    def _spin_disk_plots(self, idx="all"):
        """Generate spin disk plots

        Parameters
        ----------
        idx: int, optional
            The indicies of the results files that you wish to be included
            in the comparsion plots.
        """
        import seaborn

        palette = seaborn.color_palette(
            palette="pastel", n_colors=len(self.samples))
        parameters = ["a_1", "a_2", "tilt_1", "tilt_2"]
        for num, i in enumerate(self.parameters):
            if not all(all(j in k for k in self.parameters) for j in parameters):
                logger.warn("Failed to generate spin disk plots for %s because "
                            "%s are not in the result file" % (
                                self.labels[num], " and ".join(parameters)))
                continue
            try:
                ind = [i.index(j) for j in parameters]
                samples = [[k[idx] for k in self.samples[num]] for idx in ind]
                fig = pub.spin_distribution_plots(
                    parameters, samples, self.labels[num], palette[num])
                fig.savefig("%s/publication/spin_disk_plot_%s.png" % (
                    self.savedir, self.labels[num]))
                plt.close()
            except Exception as e:
                logger.warn("Failed to generate a spin disk plot for %s" % (
                            self.labels[num]))
                continue

    def _pepredicates_plot(self, idx):
        """Generate plots with the PEPredicates package
        """
        from pesummary.gw.pepredicates import PEPredicates

        fig = PEPredicates.plot(
            self.samples[idx], self.parameters[idx], population_prior=False)
        plt.savefig("%s/plots/%s_default_predicates.png" % (self.webdir, self.labels[idx]))
        plt.close()
        fig = PEPredicates.plot(
            self.samples[idx], self.parameters[idx], population_prior=True)
        plt.savefig("%s/plots/%s_population_predicates.png" % (self.webdir, self.labels[idx]))
        plt.close()


def main():
    """Top level interface for `summaryplots`
    """
    parser = command_line()
    insert_gwspecific_option_group(parser)
    opts = parser.parse_args()
    func = functions(opts)
    args = func["input"](opts)
    func["PlotGeneration"](args)


if __name__ == "__main__":
    main()
