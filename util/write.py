import os

class TSVWriter:

    def __init__(self, subj_num, dir = 'logs'):
        '''
        opens a file in which to log subject history
        '''
        if not os.path.exists(dir):
            os.makedirs(dir)
        fpath = os.path.join(dir, 'subject%d.tsv'%subj_num)
        self._f = open(fpath, 'w')
        self._f.write('trial_type\ttrial\tdelay\tsentence\tdetected\tstart\tend')

    def write(self, block_name, trial_num, delay, stimulus, detected, start_t, end_t):
        '''
        writes a trial's parameters to log
        '''
        line = '\n%s\t%d\t%d\t%s\t%d\t%s\t%s'%(block_name, trial_num, delay, stimulus, detected, start_t, end_t)
        self._f.write(line)

    def close(self):
        self._f.close()

    def __del__(self):
        self.close()
