"""MESSENGER UVVS data class"""
import numpy as np
import pandas as pd
from astropy import units as u

import bokeh.plotting as bkp
from bokeh.models import (HoverTool, Whisker, CDSView, BooleanFilter,
                          ColorBar, LinearColorMapper)
from bokeh.models.tickers import SingleIntervalTicker, DatetimeTicker
from bokeh.layouts import column
from bokeh.palettes import Set1, Turbo256
from bokeh.io import export_png, curdoc
from bokeh.themes import Theme

from nexoclom import Input, Output, LOSResult
from .database_setup import database_connect
from mathMB import fit_model


class InputError(Exception):
    """Raised when a required parameter is not included."""
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class MESSENGERdata:
    """Retrieve MESSENGER data from database.
    Given a species and set of comparisons, retrieve MESSSENGER UVVS
    data from the database. The list of searchable fields is given at
    :doc:`database_fields`.
    
    Returns a MESSENGERdata Object.
    
    **Parameters**
    
    species
        Species to search. This is required because the data from each
        species is stored in a different database table.
        
    query
        A SQL-style list of comparisons.
        
    The data in the object created is extracted from the database tables using
    the query:
    
    ::
    
        SELECT *
        FROM <species>uvvsdata, <species>pointing
        WHERE <query>
    
    See examples below.
    
    **Class Atributes**
    
    species
        The object can only contain a single species.
        
    frame
        Coordinate frame for the data, either MSO or Model.
        
    query
        SQL query used to search the database and create the object.
    
    data
        Pandas dataframe containing result of SQL query. Columns in the
        dataframe are the same as in the database except *frame* and
        *species* have been dropped as they are redundant. If models have been
        run, there are also columns in the form modelN for the Nth model run.
        
    taa
        Median true anomaly for the data in radians.
        
    model_label
        If *N* models have been run, this is a dictionary in the form
        `{'model0':label0, ..., 'modelN':labelN}` containing descriptions for
        the models.
        
    model_strength
        If *N* models have been run, this is a dictionary in the form
        `{'model0':strength0, ..., 'modelN':strengthN}` containing modeled
        source rates in units of :math:`10^{23}` atoms/s.
        
    **Examples**
    
    1. Loading data
    
    ::
    
        >>> from MESSENGERuvvs import MESSENGERdata
        
        >>> CaData = MESSENGERdata('Ca', 'orbit = 36')
        
        >>> print(CaData)
        Species: Ca
        Query: orbit = 36
        Frame: MSO
        Object contains 581 spectra.
        
        >>> NaData = MESSENGERdata('Na', 'orbit > 100 and orbit < 110')
        
        >>> print(NaData)
        Species: Na
        Query: orbit > 100 and orbit < 110
        Frame: MSO
        Object contains 3051 spectra.
        
        >>> MgData = MESSENGERdata('Mg',
                'loctimetan > 5.5 and loctimetan < 6.5 and alttan < 1000')
        
        >>> print(len(MgData))
        45766
        
    2. Accessing data.
    
    * The observations are stored within the MESSENGERdata object in a
      `pandas <https://pandas.pydata.org>`_ dataframe attribute called *data*.
      Please see the `pandas documentation <https://pandas.pydata.org>`_ for
      more information on how to work with dataframes.
    
    ::
    
        >>> print(CaData.data.head(5))
                                 utc  orbit  merc_year  ...  loctimetan         slit               utcstr
        unum                                            ...
        3329 2011-04-04 21:24:11.820     36          0  ...   14.661961  Atmospheric  2011-04-04T21:24:11
        3330 2011-04-04 21:25:08.820     36          0  ...   12.952645  Atmospheric  2011-04-04T21:25:08
        3331 2011-04-04 21:26:05.820     36          0  ...   12.015670  Atmospheric  2011-04-04T21:26:05
        3332 2011-04-04 21:27:02.820     36          0  ...   12.007919  Atmospheric  2011-04-04T21:27:02
        3333 2011-04-04 21:27:59.820     36          0  ...   12.008750  Atmospheric  2011-04-04T21:27:59
        
        [5 rows x 29 columns]

    * Individual observations can be extracted using standard Python
      slicing techniques:
     
    ::
        
        >>> print(CaData[3:8])
        Species: Ca
        Query: orbit = 36
        Frame: MSO
        Object contains 5 spectra.

        >>> print(CaData[3:8].data['taa'])
        unum
        3332    1.808107
        3333    1.808152
        3334    1.808198
        3335    1.808243
        3336    1.808290
        Name: taa, dtype: float64

    3. Modeling data
    
    ::
    
        >>> inputs = Input('Ca.spot.Maxwellian.input')
        >>> CaData.model(inputs, 1e5, label='Model 1')
        >>> inputs..speeddist.temperature /= 2.  # Run model with different temperature
        >>> CaData.model(inputs, 1e5, label='Model 2')
        
    4. Plotting data
    
    ::
    
        >>> CaData.plot('Ca.orbit36.models.html')
    
    5. Exporting data to a file
    
    ::
    
        >>> CaData.export('modelresults.csv')
        >>> CaData.export('modelresults.html', columns=['taa'])

    
    """
    def __init__(self, species=None, comparisons=None):
        allspecies = ['Na', 'Ca', 'Mg']
        self.species = None
        self.frame = None
        self.query = None
        self.data = None
        self.taa = None
        self.inputs = None
        self.model_info = None
        
        if species is None:
            pass
        elif species not in allspecies:
            # Return list of valid species
            print(f"Valid species are {', '.join(allspecies)}")
        elif comparisons is None:
            # Return list of queryable fields
            with database_connect() as con:
                columns = pd.read_sql(
                    f'''SELECT * from {species}uvvsdata, {species}pointing
                        WHERE 1=2''', con)
            print('Available fields are:')
            for col in columns.columns:
                print(f'\t{col}')
        else:
            # Run the query and try to make the object
            query = f'''SELECT * from {species}uvvsdata, {species}pointing
                        WHERE unum=pnum and {comparisons}
                        ORDER BY unum'''
            try:
                with database_connect() as con:
                    data = pd.read_sql(query, con)
            except Exception:
                raise InputError('MESSENGERdata.__init__',
                                 'Problem with comparisons given.')

            if len(data) > 0:
                self.species = species
                self.frame = data.frame[0]
                self.query = comparisons
                data.drop(['species', 'frame'], inplace=True, axis=1)
                data.loc[data.alttan < 0, 'alttan'] = 1e10
                self.data = data
                self.data.set_index('unum', inplace=True)
                self.taa = np.median(data.taa)
            else:
                print(query)
                print('No data found')
                
    def __str__(self):
        result = (f'Species: {self.species}\n'
                  f'Query: {self.query}\n'
                  f'Frame: {self.frame}\n'
                  f'Object contains {len(self)} spectra.')
        return result

    def __repr__(self):
        result = ('MESSENGER UVVS Data Object\n'
                  f'Species: {self.species}\n'
                  f'Query: {self.query}\n'
                  f'Frame: {self.frame}\n'
                  f'Object contains {len(self)} spectra.')
        return result

    def __len__(self):
        try:
            return len(self.data)
        except Exception:
            return 0

    def __getitem__(self, q_):
        if isinstance(q_, int):
            q = slice(q_, q_+1)
        elif isinstance(q_, slice):
            q = q_
        elif isinstance(q_, pd.Series):
            q = np.where(q_)[0]
        else:
            raise TypeError

        new = MESSENGERdata()
        new.species = self.species
        new.frame = self.frame
        new.query = self.query
        new.taa = self.taa
        new.data = self.data.iloc[q].copy()
        new.model_info = self.model_info
        new.inputs = self.inputs

        return new

    def __iter__(self):
        for i in range(len(self.data)):
            yield self[i]

    def keys(self):
        """Return all keys in the object, including dataframe columns"""
        keys = list(self.__dict__.keys())
        keys.extend([f'data.{col}' for col in self.data.columns])
        return keys

    def set_frame(self, frame=None):
        """Convert between MSO and Model frames.

        More frames could be added if necessary.
        If Frame is not specified, flips between MSO and Model."""
        if (frame is None) and (self.frame.upper() == 'MSO'):
            frame = 'Model'
        elif (frame is None) and (self.frame.upper() == 'MODEL'):
            frame = 'MSO'
        else:
            pass

        allframes = ['MODEL', 'MSO']
        if frame.upper() not in allframes:
            print('{} is not a valid frame.'.format(frame))
            return None
        elif frame == self.frame:
            pass
        elif (self.frame.upper() == 'MSO') and (frame.upper() == 'MODEL'):
            # Convert from MSO to Model
            self.data.x, self.data.y = self.data.y.copy(), -self.data.x.copy()
            self.data.xbore, self.data.ybore = (self.data.ybore.copy(),
                                                -self.data.xbore.copy())
            self.data.xtan, self.data.ytan = (self.data.ytan.copy(),
                                              -self.data.xtan.copy())
            self.frame = 'Model'
        elif (self.frame.upper() == 'MODEL') and (frame.upper() == 'MODEL'):
            self.data.x, self.data.y = -self.data.y.copy(), self.data.x.copy()
            self.data.xbore, self.data.ybore = (-self.data.ybore.copy(),
                                                self.data.xbore.copy())
            self.data.xtan, self.data.ytan = (-self.data.ytan.copy(),
                                              self.data.xtan.copy())
            self.frame = 'MSO'
        else:
            assert 0, 'You somehow picked a bad combination.'

    def model(self, start_from, npackets, quantity='radiance',
              fit_method='chisq', dphi=3*u.deg, overwrite=False,
              masking=None, filenames=None, label=None,
              fit_to_data=False):
        """Run the nexoclom model with specified inputs and fit to the data.
        
        ** Parameters**
        inputs
            A nexoclom Input object or a string with the path to an inputs file.
            
        npackets
            Number of packets to run.
            
        fit_method
            Allows user to specify the quantity to be minimized when fitting
            the model to the data. Default = chisq (chi-squared
            minimization). Other option is 'difference' which minimizes the
            sum of the differences of the data and the model ignoring the
            data uncertainty.
            
        dphi
            Angular size of the view cone. Default = 3 deg. Must be
            given as an astropy quantity.
            
        overwrite
            Set to True to erase any previous model runs with these inputs.
            Default = False
        
        masking
            Allows user to specify which data points are included in the fit
            to the model. Default = None
            * middleX: Use the middle X% of values. For example, middle50
              excludes the faintest and brightest 25% spectra
            
            * minsnrX: specifies the minimum signal-to-noise ratio to use.
              minsnr3 exludes any spectra with SNR < 3
            
            * siglimitX: Excludes any data where the model is not within X σ
              of the data in an initial fit to the data.
        """

        runmodel = True
        if isinstance(start_from, str):
            inputs = Input(start_from)
            output = None
        elif isinstance(start_from, Input):
            inputs = start_from
            output = None
        elif isinstance(start_from, Output):
            inputs = start_from.inputs
            output = start_from
            runmodel = False
        else:
            raise InputError('MESSENGERdata.model', 'Problem with the inputs.')

        # TAA needs to match the data
        oldtaa = inputs.geometry.taa
        if len(self.data.orbit.unique()) == 1:
            inputs.geometry.taa = np.median(self.data.taa)*u.rad
        elif self.data.taa.max()-self.data.taa.min() < 3*np.pi/180.:
            inputs.geometry.taa = self.data.taa.median()*u.rad
        else:
            assert 0, 'Too wide a range of taa'
            
        # If using a planet-fixed source map, need to set subsolarlon
        if ((inputs.spatialdist.type == 'surface map') and
            (inputs.spatialdist.coordinate_system == 'planet-fixed')):
            inputs.spatialdist.subsolarlon = self.data.subslong.median()*u.rad
        else:
            pass

        # Run the model
        self.set_frame('Model')
        if runmodel:
            inputs.run(npackets, overwrite=overwrite)
            model_result = LOSResult(inputs, self, quantity, dphi=dphi,
                                     filenames=filenames, overwrite=overwrite,
                                     masking=masking, fit_to_data=fit_to_data)
        else:
            model_result = LOSResult(output, self, quantity, dphi=dphi,
                                     filenames=filenames, overwrite=overwrite,
                                     fit_method=fit_method, masking=masking,
                                     fit_to_data=fit_to_data)

        # Simulate the data
        if self.inputs is None:
            self.inputs = [inputs]
        else:
            self.inputs.append(inputs)

        # modkey is the number for this model
        modkey = f'model{len(self.inputs)-1:00d}'
        npackkey = f'npackets{len(self.inputs)-1:00d}'
        maskkey = f'mask{len(self.inputs)-1:00d}'
        self.data[modkey] = model_result.radiance/1e3 # Convert to kR
        self.data[npackkey] = model_result.ninview

        strength, goodness_of_fit, mask = fit_model(self.data.radiance.values,
                                                    self.data[modkey].values,
                                                    self.data.sigma.values,
                                                    fit_method=fit_method,
                                                    masking=masking,
                                                    altitude=self.data.alttan)
        strength *= u.def_unit('10**23 atoms/s', 1e23/u.s)
        
        self.data[modkey] = self.data[modkey]*strength.value
        self.data[maskkey] = mask

        if label is None:
            label = modkey.capitalize()
        else:
            pass

        model_info = {'fit_method': fit_method,
                      'goodness-of-fit': goodness_of_fit,
                      'strength': strength,
                      'label': label,
                      'filenames': model_result.filenames,
                      'fitted': model_result.fitted}
        if self.model_info is None:
            self.model_info = {modkey: model_info}
        else:
            self.model_info[modkey] = model_info
        
        print(f'Model strength for {label} = {strength}')

        # Put the old TAA back in.
        inputs.geometry.taa = oldtaa
    
    def plot(self, filename=None, show=True, **kwargs):
        curdoc().theme = Theme('bokeh.yml')
    
        if filename is not None:
            if not filename.endswith('.html'):
                filename += '.html'
            else:
                pass
            bkp.output_file(filename)
        else:
            pass
    
        # Format the date correction
        self.data['utcstr'] = self.data['utc'].apply(
                lambda x:x.isoformat()[0:19])
    
        # Put the dataframe in a useable form
        self.data['lower'] = self.data.radiance-self.data.sigma
        self.data['upper'] = self.data.radiance+self.data.sigma
        self.data['lattandeg'] = self.data.lattan*180/np.pi
    
        source = bkp.ColumnDataSource(self.data)
    
        # Tools
        tools = ['pan', 'box_zoom', 'wheel_zoom', 'xbox_select',
                 'hover', 'reset', 'save']
    
        # tool tips
        tips = [('index', '$index'),
                ('UTC', '@utcstr'),
                ('Radiance', '@radiance{0.2f} kR'),
                ('LTtan', '@loctimetan{2.1f} hr'),
                ('Lattan', '@lattandeg{3.1f} deg'),
                ('Alttan', '@alttan{0.f} km')]
    
        # Make the figure
        width, height = 1200, 600
        fig0 = bkp.figure(plot_width=width, plot_height=height,
                          x_axis_type='datetime',
                          title=f'{self.species}, {self.query}',
                          x_axis_label='UTC',
                          y_axis_label='Radiance (kR)',
                          y_range=[0, self.data.radiance.max()*1.5],
                          tools=tools)
    
        # plot the data
        dplot = fig0.circle(x='utc', y='radiance', size=7, color='black',
                            legend_label='Data', hover_color='yellow',
                            source=source, selection_color='orange')
        fig0.line(x='utc', y='radiance', color='black', legend_label='Data',
                  source=source)
        fig0.xaxis.ticker = DatetimeTicker(num_minor_ticks=5)
    
        # Add error bars
        fig0.add_layout(Whisker(source=source, base='utc', upper='upper',
                                lower='lower'))
        renderers = [dplot]
    
        # Plot the model
        col = (c for c in Set1[9])
        if self.model_info is not None:
            modplots, maskedplots = [], []
            for modkey, info in self.model_info.items():
                try:
                    c = next(col)
                except StopIteration:
                    col = (c for c in Set1[9])
                    c = next(col)
            
                label = f"{info['label']}, {info['strength'].value:0.2f} * 10**23 atoms/s"
                fig0.line(x='utc', y=modkey, source=source,
                          legend_label=label, color=c)
                modplots.append(fig0.circle(x='utc', y=modkey, size=7, color=c,
                                            source=source, legend_label=label))
                maskkey = modkey.replace('model', 'mask')
                mask = np.logical_not(self.data[maskkey]).to_list()
                view = CDSView(source=source, filters=[BooleanFilter(mask)])
                maskedplots.append(fig0.circle(x='utc', y=modkey, size=7,
                                               source=source, line_color=c,
                                               fill_color='yellow', view=view,
                                               legend_label=label))
                renderers.extend(modplots)
                renderers.extend(maskedplots)
    
        datahover = HoverTool(tooltips=tips, renderers=renderers)
        fig0.add_tools(datahover)
    
        ##############
        # Plot tangent point
        m = self.data[self.data.alttan != self.data.alttan.max()].alttan.max()
        col = np.interp(self.data.alttan, np.linspace(0, m, 256),
                        np.arange(256)).astype(int)
        source.add([Turbo256[c] for c in np.floor(col)], name='color')
    
        color_mapper = LinearColorMapper(palette="Turbo256", low=0, high=m)
    
        width, height = 1200, 600
        tools = ['pan', 'box_zoom', 'wheel_zoom', 'box_select',
                 'hover', 'reset', 'save']
        fig1 = bkp.figure(plot_width=width, plot_height=height,
                          title=f'Tangent Point Location',
                          x_axis_label='Local Time (hr)',
                          y_axis_label='Latitude (deg)',
                          x_range=[0, 24],
                          y_range=[-90, 90], tools=tools)
        tanplot = fig1.circle(x='loctimetan', y='lattandeg', size=5,
                              selection_color='orange', hover_color='purple',
                              source=source, color='color')
        fig1.xaxis.ticker = SingleIntervalTicker(interval=6,
                                                 num_minor_ticks=6)
        fig1.yaxis.ticker = SingleIntervalTicker(interval=45,
                                                 num_minor_ticks=3)
        color_bar = ColorBar(color_mapper=color_mapper, title='Altitude (km)',
                             label_standoff=12, border_line_color=None,
                             location=(0, 0))
        fig1.add_layout(color_bar, 'right')
        datahover = HoverTool(tooltips=tips, renderers=[tanplot])
        fig1.add_tools(datahover)
    
        grid = column(fig0, fig1)
    
        if filename is not None:
            bkp.output_file(filename)
            export_png(grid, filename=filename.replace('.html', '.png'))
            bkp.save(grid)
        else:
            pass
    
        if show:
            bkp.show(grid)
    
        return fig0, fig1

    def export(self, filename, columns=('utc', 'radiance')):
        """Export data and models to a file.
        **Parameters**
        
        filename
            Filename to export model results to. The file extension determines
            the format. Formats available: csv, pkl, html, tex
            
        columns
            Columns from the data dataframe to export. Available columns can
            be found by calling the `keys()` method on the data object.
            Default = ['utc', 'radiance'] and all model result columns. Note:
            The default columns are always included in the output
            regardless of whether they are specified.
        
        **Returns**
        
        No outputs.
        
        """
        columns_ = list(columns)
        if self.model_info is not None:
            columns_.extend(self.model_info.keys())
        else:
            pass
        
        # Make sure radiance is in there
        if 'radiance' not in columns_:
            columns_.append('radiance')
        else:
            pass

        # Make sure UTC is in there
        if 'utc' not in columns_:
            columns_.append('utc')
        else:
            pass

        if len(columns_) != len(set(columns_)):
            columns_ = list(set(columns_))
        else:
            pass

        for col in columns_:
            if col not in self.data.columns:
                columns_.remove(col)
            else:
                pass

        subset = self.data[columns_]
        if filename.endswith('.csv'):
            subset.to_csv(filename)
        elif filename.endswith('.pkl'):
            subset.to_pickle(filename)
        elif filename.endswith('.html'):
            subset.to_html(filename)
        elif filename.endswith('.tex'):
            subset.to_latex(filename)
        else:
            print('Valid output formats = csv, pkl, html, tex')


