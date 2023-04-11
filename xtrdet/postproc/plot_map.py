
#%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon

# Author:  Fuxing Wang, 30 June, 2019
# Reference: https://jakevdp.github.io/PythonDataScienceHandbook/04.13-geographic-data-with-basemap.html
# 	     https://basemaptutorial.readthedocs.io/en/latest/subplots.html

class PlotMap(object):

    def __init__(self, proj_def, res_def, 
		width_def, height_def, lat_0_def, lon_0_def, nsubplot):
        self.proj_def = proj_def
        self.res_def = res_def
        self.width_def = width_def
        self.height_def = height_def
        self.lat_0_def = lat_0_def
        self.lon_0_def = lon_0_def
        self.nsubplot = nsubplot
        if self.nsubplot == 6:
            self.fig = plt.figure(figsize=(7, 12)) # width, height
        elif self.nsubplot == 4:
            self.fig = plt.figure(figsize=(7, 9)) # width, height
        elif self.nsubplot == 2:
            self.fig = plt.figure(figsize=(7, 5)) # width, height
        #self.Plot_Basemap()


    def plot_basemap(self):
	# Draw the map background

        if self.proj_def == 'ortho':
            m = Basemap(projection = self.proj_def, resolution = self.res_def, 
                lat_0 = self.lat_0_def, lon_0 = self.lon_0_def)
            m.bluemarble(scale=0.5);

        elif self.proj_def == 'lcc':
            m = Basemap(projection = self.proj_def, resolution = self.res_def,
                width = self.width_def, height = self.height_def, 
                lat_0 = self.lat_0_def, lon_0 = self.lon_0_def,)
	    #m.etopo(scale=0.5, alpha=0.5)  # the green background
	    #m.bluemarble(scale=0.5)

        elif self.proj_def == 'cyl':
            m = Basemap(projection = self.proj_def, resolution = self.res_def,
                llcrnrlat = self.lat_0_def - 1.0, urcrnrlat = self.lat_0_def + 1.0,
                llcrnrlon = self.lon_0_def - 1.0, urcrnrlon = self.lon_0_def + 1.0,)
            #m.etopo(scale=0.5, alpha=0.5)

	#m.shadedrelief()
	#m.shadedrelief(scale=0.5) # the green background
        m.drawcoastlines(color='gray')
        m.drawcountries(color='gray')
        m.drawstates(color='gray')
        self.m = m


    def plot_point(self, lat, lon, var_to_plot, scale_min_def, scale_max_def, fig_name):

        #self.Plot_Basemap()

        # Scatter data, with color reflecting var_to_plot
        sca_size = 5
        cmap_def = 'Greens'  #Reds
        alpha_def = 0.9
        self.m.scatter(lon, lat, latlon=True,
            #c=np.log10(population), s=area,
            c=var_to_plot, s=sca_size,
            cmap=cmap_def, alpha=alpha_def)

        # Create colorbar and legend
        #plt.colorbar(label=r'$\log_{10}({\rm population})$')
        #plt.colorbar(label=r'$({ppp})$')
        plt.clim(scale_min_def, scale_max_def)

        """
        # make legend with dummy points
        for a in [1, 3, 5]:
            plt.scatter([], [], c='k', alpha=0.5, s=a,
            label=str(a) + ' km$^2$')
        plt.legend(scatterpoints=1, frameon=False,
            labelspacing=1, loc='lower left');

        """
        self.fig.savefig(fig_name)

        # Map (long, lat) to (x, y) for plotting
        #x, y = m(-122.3, 47.6)
        #plt.plot(x, y, 'ok', markersize=5)
        #plt.text(x, y, ' Seattle', fontsize=12);
        ##self.text(0.5, 0.95, figtitle, ha='center')


    def plot_marker(self, lat, lon, scale_min_def, scale_max_def, sta_name, fig_name):
        # https://stackoverflow.com/questions/14432557/matplotlib-scatter-plot-with-different-text-at-each-data-point
        # https://stackoverflow.com/questions/38830184/plotting-text-on-basemap

        # Scatter data, with color reflecting var_to_plot
        sca_size = 2
        self.m.scatter(lon, lat, latlon=True,
            #c=np.log10(population), s=area,
            s=sca_size, color = 'red', 
            cmap='Reds', alpha=0.5)

        # Create colorbar and legend
        #plt.colorbar(label=r'$({ppp})$')
        plt.clim(scale_min_def, scale_max_def)

        sta_name_to_plot = ['2', '2', '3', '3', '5', '6', '6', '7', '8', '5'] 
        n = range(len(lon))  
        for i, txt in enumerate(n):
            txt = sta_name_to_plot[i]
            print (i, lon[i], lat[i], txt)
            #self.m.annotate(txt, (lon[i], lat[i]))
            plt.annotate(txt, self.m(lon[i], lat[i]), ha='left', va='top', size=6)

        #plt.xlabel("")
        self.fig.savefig(fig_name)


    def plot_2dfield(self, lat, lon, var2d_to_plot, scale_min_def, scale_max_def, \
        title_def, cmap_def, fontsize_def, isubplot = 1):

        #if np.array(lat).dim == 1 and np.array(lon).dim == 1:  
        #    lon, lat = np.meshgrid(lon, lat)

        #var2d_to_plot_mask = np.ma.masked_where(np.isnan(var2d_to_plot),var2d_to_plot)

        if self.nsubplot == 4:
            ax = self.fig.add_subplot(2,2,isubplot)
        elif self.nsubplot == 6:
            ax = self.fig.add_subplot(3,2,isubplot)
        elif self.nsubplot == 2:
            ax = self.fig.add_subplot(1,2,isubplot)
        self.plot_basemap()

        self.m.pcolormesh(lon, lat, var2d_to_plot,
            latlon=True, cmap=cmap_def, vmin=scale_min_def, vmax=scale_max_def)

        #plt.clim(scale_min_def, scale_max_def)

        self.m.drawcoastlines(color='lightgray')

        plt.title(title_def, fontsize=fontsize_def)


    def plot_colorbar(self, label_def, extend_def, isubplot = 1):

        plt.subplots_adjust(left=0, bottom=0.02, right=1.0, top=1.0)
        cax = {}
        if self.nsubplot == 6:
            cax[0] = plt.axes([0.1, 0.05, 0.8, 0.02]) #left, bottom, width, height
        elif self.nsubplot == 4:
            cax[0] = plt.axes([0.1, 0.03, 0.8, 0.02]) #left, bottom, width, height
        elif self.nsubplot == 2:
            #cax = plt.axes([0.1, 0.08, 0.8, 0.02]) #left, bottom, width, height
            cax[0] = plt.axes([0.05, 0.08, 0.4, 0.02]) #left, bottom, width, height
            cax[1] = plt.axes([0.55, 0.08, 0.4, 0.02]) #left, bottom, width, height
        cb = plt.colorbar(label=label_def, cax=cax[isubplot-1], orientation='horizontal', extend=extend_def)

        #cb=plt.colorbar(label=label_def, pad=0.02, shrink=0.8, extend=extend_def)
        #cb=plt.colorbar(label=label_def, orientation='horizontal', pad=0.02, shrink=0.8, extend=extend_def)
        ##cb.colorbar().set_label(label=label_def, size=15)
        #cb.set_label(label_def, fontsize=10)
        #cb.ax.tick_params(labelsize=10)
        

    def plot_save(self, fig_name):
        #self.fig.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
        # rect: (left, bottom, right, top). A rectangle in normalized figure coordinates into which the whole subplots area (including labels) will fit.
        
        if self.nsubplot == 6:
            self.fig.tight_layout(rect=[0, 0.05, 1.00, 1.00]) #pad=0, w_pad=0.0, h_pad=0.0) #, rect=[0, -0.1, 1.00, 1.05])
        elif self.nsubplot == 4:
            self.fig.tight_layout(rect=[0, 0.04, 1.00, 1.00]) #pad=0, w_pad=0.0, h_pad=0.0) #, rect=[0, -0.1, 1.00, 1.05])
        elif self.nsubplot == 2:
            self.fig.tight_layout(rect=[0, 0.03, 1.00, 1.00]) #pad=0, w_pad=0.0, h_pad=0.0) #, rect=[0, -0.1, 1.00, 1.05])

        self.fig.tight_layout()
        self.fig.savefig(fig_name)


    def draw_screen_poly(self, lats, lons, edgecolor):
        x, y = self.m( lons, lats )
        xy = list(zip(x,y))
        #poly = Polygon( xy,alpha=0.1,edgecolor='k',linewidth=1 )
        poly = Polygon( xy, edgecolor=edgecolor, linewidth=3, facecolor='none')
        plt.gca().add_patch(poly)


    def get_scale(self, data):
        #for key, value in data.items():
            
        pass
