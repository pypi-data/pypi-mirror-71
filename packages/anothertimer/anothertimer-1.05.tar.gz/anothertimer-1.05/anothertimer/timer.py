from typing import List, Dict
import time
import os
import csv

class Timer:
    def __init__(self):
        """
        Creates a timer object. Example initialization timer = Timer().
        """
        # start and end time
        self.t:List[float, float] = [0., 0.]
        
        # storing time
        self.t_store:Dict = {'0': []}        
        
        # current mode (either True or False)
        self._mode = False
    
    def _store(self, section:str='default'):
        """
        Store the result of tic and toc into the t_store dict.
        
        Args:
            section (str): which section to store result in. If not set,
                use the newest section.
        """
        # if 'default' get the last key in the t_store dict
        if section == 'default':
            section = list(self.t_store.keys())[-1]
        
        # store the result in the dict
        self.t_store[section].append([self.t[0], self.t[1], 
                             self.t[1] - self.t[0]])
    
    def _clean_up_tstore(self):
        """
        Remove all keys with empty lists.
        """
        empty_keys = []
        for key, value in self.t_store.items():
            if len(value) == 0:
                empty_keys.append(key)
        [self.t_store.pop(key) for key in empty_keys]
    
    def tac(self, section:str='default'):
        """
        Start a new section for timing.
        
        Args:
            section (str): name of the new section to store result. If nothing
                is set, a new section named by the index will be created.
        """
        # if no section name is set, use the next index number as key
        if section == 'default':
            section = str(len(self.t_store.keys()) + 1)
            
        # create new section
        self.t_store[section] = []
        
    def tic(self, section:str='default') -> float:
        """
        Begin the timer. If timer already running, act as stopwatch instead (
            record the time, does not reset like toc does).
        
        Args:
            section (str): section to put the result in (only applicable for
                stopwatch mode). If not specified, use the newest section.
        
        Returns:
            float: time elapsed since first tic.
        """
        # tic as a starting timer
        if self._mode == False:
            # cannot define section name when use tic to start
            if section != 'default':
                raise ValueError('Cannot define section name here')
            
            # store the starting time
            self.t[0] = time.time()
            self._mode = True
            
            return 0.0
        # tic as a stopwatch
        else:
            # store the lap time
            self.t[1] = time.time()
            self._store(section)
            
            return self.t[1] - self.t[0]
                    
    def toc(self, section:str='default') -> float:
        """
        End the timer and store the time.
        
        Args:
            section (str): section to put the result in. If not specified, use
                the newest section.

        Returns:
            float: time elapsed since first tic.
        """
        # store the end time        
        self.t[1] = time.time()
        self._store(section)
        
        # reset
        self._mode = False
        runtime = self.t[1] - self.t[0]
        self.t:List[float, float] = [0., 0.]    

        return runtime
    

    def dump(self, filename:str, mode:str = 'a'):        
        """
        Store all recorded run times in a file.

        Args:
            filename (str): saving file name.
            mode (str, optional): File write mode. Either 'a' for append or
                'w' for write. Defaults to 'a'.
        """
        
        # make sure we got the correct output mode            
        assert(mode == 'a' or mode == 'w')
        
        # output to the saving file
        save_output:str = ''             
        
        # clean up tstore to remove empty sections
        self._clean_up_tstore()
        
        # add to the output
        for name, tlist in self.t_store.items():
            for time_list in tlist:
                runtime = time_list[1] - time_list[0]
                save_output += f'{name},{time_list[0]},{time_list[1]},{runtime}\n'
        
        # write the output
        f = open(filename, f'{mode}+')
        f.write(save_output)
        f.close()
    
    def load(self, filename:str) -> Dict:
        """
        Read all recorded run times into t_store dict. Note that this adds on
            to the t_store dictionary.     

        Args:
            filename (str): file to read.

        Returns:
            Dict: the loaded t_store dictionary.
        """

        data = csv.reader(open(filename), delimiter=',')
        
        for row in list(data):
            if row[0] not in self.t_store.keys():
                self.t_store[row[0]] = []
            self.t_store[row[0]].append(list(map(float, row[1:])))
        
        return self.t_store
    
    def plot(self, plot_start_time:bool = True,
             plot_avg:bool = False):
        """
        For plotting the runtimes. Needs matplotlib. Causes additional overhead
        due to matplotlib plotting. Use discriminately.

        Args:
            plot_start_time (bool, optional): Second x-axis for labeling the 
                local start time. Defaults to True.
            plot_avg (bool, optional): Plot the average time as a dashed line. 
                Defaults to False.

        Returns:
            fig, ax: Figure and axes objects from matplotlib.
        """
        
        # import matplotlib for plotting
        import matplotlib.pyplot as plt
        
        # clean up the t_store dict
        self._clean_up_tstore()
        
        # set up for plotting
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(111)
        ax.set_ylabel('Run time (s)')
        ax.set_xlabel('Run number')
        for name, tlist in self.t_store.items():
            # unzip the data structure
            start_t, _, runtime = zip(*tlist)
            
            # cast to make sure the runtimes are float
            runtime = list(map(float, runtime))
            # how many times we ran this
            run_number = list(range(len(runtime)))
                       
            # plotting
            p =ax.plot(run_number, runtime, '.-', label=f'{name}')
            
            if plot_start_time:
                # prepare the start time
                # convert from time.time() seconds --> date time format
                start_local = []
                for i, t in enumerate(start_t):
                    t = float(t)
                    # convert time to local time structure
                    local_t = time.localtime(t)
                    # format the time showing DD/MM HH:MM:SS
                    formatted_t = time.strftime("%d/%m %H:%M:%S", local_t)
                    # if this is the first label, we are okay
                    # else this is too much information (don't need DD/MM)
                    if i > 0:
                        # check the previous time
                        prev_t = time.localtime(float(start_t[i-1]))
                        # if the current time and previous time share DD/MM
                        if (prev_t.tm_mon == local_t.tm_mon and 
                            prev_t.tm_mday == local_t.tm_mday):
                            # then don't show DD/MM
                            formatted_t = time.strftime("%H:%M:%S", local_t)
                    start_local.append(formatted_t)        
                
                # plotting
                ax2 = ax.twiny()
                l2, = ax2.plot(start_local, runtime, 'k.-', label=f'Section {name}')
                ax2.set_xlabel('Start time (DD/MM HH:MM:SS)')
                ax2.set_xticklabels(start_local, rotation=90)
                l2.remove()
            
            if plot_avg:
                from statistics import mean
                ax.axhline(mean(runtime),color=p[0].get_color(),linestyle=':')
        
        # turn on grid
        ax.grid()
        # make sure everything fits
        fig.tight_layout()
        ax.legend()
        
        return fig, ax
    
    def summarize(self) -> str:
        """
        Output in a table format with columns start time, end time, elapsed
        time.
        
        Returns:
            str: the summarized timing result.
        """
        from statistics import mean, stdev
        
         # formatting to a table form
        fmt = '{: >15}  {: >15} {: >15}\n'
        output:str = '\nDatetime format: DD/MM HH:MM:SS\n'
        output += fmt.format('Start', 'End','Time (s)')
        
        # clean up the t_store dict
        self._clean_up_tstore()
        
        # loop through the dict
        for name, tlist in self.t_store.items():
            output += f'\nSection: {name}\n'    
            # unzip the data structure
            start_t, end_t, runtime = zip(*tlist)
            runtime = list(map(float, runtime))
            
            for i, t in enumerate(start_t):
                # convert time to local time for start_t
                t = float(t)
                local_t = time.localtime(t)
                t1 = time.strftime("%d/%m %H:%M:%S", local_t)
                # convert time to local time for end_t
                t = float(end_t[i])
                local_t = time.localtime(t)
                t2 = time.strftime("%d/%m %H:%M:%S", local_t)
                # output
                output +=  fmt.format(t1, t2, 
                                    round(runtime[i],6))
            
            # print some basic stats
            output += f'Mean: {round(mean(runtime),6)}\n'
            output += f'Std. Dev.: {round(stdev(runtime),6)}\n'

        return output
    
    def __str__(self):
        return self.summarize()
    