from collections import OrderedDict as odict
import pylab as plt
import iris

from omnium.processes import PylabProcess
from omnium.stash import stash

OPTS = odict([(12, {182: {'l': 'Adv.', 'fmt': 'r-'}}),
             (9, {182: {'l': 'BL+cloud', 'fmt': 'r--'}}),
             (4, {182: {'l': 'LS rain', 'fmt': 'b--'}}),
             (30, {182: {'l': 'Total', 'fmt': 'k-'}})])


class PlotLastMoistProfile(PylabProcess):
    name = 'plot_last_moist_profile'
    out_ext = 'png'

    def load_upstream(self):
        super(PlotLastMoistProfile, self).load_upstream()
        filenames = [n.filename(self.config) for n in self.node.from_nodes]
        profiles = iris.load(filenames)
        self.data = profiles

    def run(self):
        super(PlotLastMoistProfile, self).run()
        profiles = self.data

        fig = plt.figure()

        if self.node.name == 'moist_profile_plots_moist_cons':
            name = 'moist. cons. on'
        elif self.node.name == 'moist_profile_plots_no_moist_cons':
            name = 'moist. cons. off'
        title = 'q increments ({})'.format(name)

        fig.canvas.set_window_title(title)

        plt.title(title)

        for k, v in OPTS.items():
            for profile in profiles:
                section = profile.attributes['STASH'].section
                item = profile.attributes['STASH'].item
                if k == section and item in v:
                    opt = v[item]
                    break

            last_profile = profile[-1]
            # stash.rename_unknown_cube(last_profile)
            # profile data is in kg/kg/dt, 1440 turns into /day, 1000 turns into g/kg/day.
            # height is in m, /1000 turns into km.
            label = opt['l']
            fmt = opt['fmt']
            plt.plot(last_profile.data * 1440 * 1000, 
                     last_profile.coord('level_height').points / 1000,
                     fmt,
                     label=label)

        plt.xlim((-10, 10))
        plt.xlabel('(g kg$^{-1}$ day$^{-1}$)')
        plt.ylabel('Height (km)')

        plt.legend(loc=2)
        self.processed_data = fig
