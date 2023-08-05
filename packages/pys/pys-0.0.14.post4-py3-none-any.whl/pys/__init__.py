'''
pys -- pythons
'''
import re;
try:
    import cPickle as pickle;
except ImportError:
    import pickle;

def conv(arg,default=None,func=None):
    '''
    essentially, the generalization of
    
    arg if arg else default

    or

    func(arg) if arg else default
    '''
    if func:
        return func(arg) if arg else default;
    else:
        return arg if arg else default;

def test(d,k):
    '''short for `k in d and d[k]', returns None otherwise.'''
    if k in d and (d[k] is not False and d[k] is not None):
        return True;

def testN(d,k):
    '''short for `k in d and d[k] is not None', returns None otherwise.'''
    if k in d and (d[k] is not None):
        return True;


def dump_pickle(name, obj):
    '''quick pickle dump similar to np.save'''
    with open(name,"wb") as f:
        pickle.dump(obj,f,2);
    pass;

def load_pickle(name):
    '''quick pickle load similar to np.load'''
    with open(name,"rb") as f:
        return pickle.load(f);
    pass;

def chunks(l,n):
    '''chunk l in n sized bits'''
    #http://stackoverflow.com/a/3226719
    #...not that this is hard to understand.
    return [l[x:x+n] for x in range(0, len(l), n)];

def subdiv(l,n):
    '''chunk l in n sized bits'''
    #http://stackoverflow.com/a/3226719
    #...not that this is hard to understand.
    sz   = len(l) // n;
    ret = [ l[i:i+sz] for i in range(0, sz*(n-1), sz) ];
    ret += [ l[sz*(n-1):] ];
    return ret;



def check_vprint(s, vprinter):
    '''checked verbose printing'''
    if vprinter is True:
        print(s);
    elif callable(vprinter):
        vprinter(s);

def mkvprint(opts):
    '''makes a verbose printer for use with docopts'''
    return lambda s: check_vprint(s,opts['--verbose']);
 
def subcall(cmd):
    '''check output into list'''
    return subprocess.check_output(cmd).split('\n');

def filelines(fname,strip=False):
    '''read lines from a file into lines...optional strip'''
    with open(fname,'r') as f:
        lines = f.readlines();
    if strip:
        lines[:] = [line.strip() for line in lines]
    return lines;

fltrx_s=r"[-+]{0,1}\d+\.{0,1}\d*(?:[eE][-+]{0,1}\d+){0,1}";
fltrx=re.compile(fltrx_s);
intrx_s=r"[-+]{0,1}\d+";
intrx=re.compile(intrx_s);
#i for identifier string. Must start with alpha+underscore.
isrx_s = r'[a-zA-Z_]+[\w ]*';
isrx=re.compile(isrx_s);
rgbrx_s = r"\( *(?:{numrx} *, *){{{rep1}}}{numrx} *,{{0,1}} *\)".format(
    rep1=2,
    numrx=fltrx_s);
colrx_s = r"(?:{isrx}|{rgbrx})".format(isrx=isrx_s,rgbrx=rgbrx_s);
colrx=re.compile(colrx_s);

def parse_utuple(s,urx,length=2):
    '''parse a string into a list of a uniform type'''
    if type(urx) != str:
        urx=urx.pattern;
    if length is not None and length < 1:
        raise ValueError("invalid length: {}".format(length));
    if length == 1:
        rx = r"^ *\( *{urx} *,? *\) *$".format(urx=urx);
    elif length is None:
        rx = r"^ *\( *(?:{urx} *, *)*{urx} *,? *\) *$".format(urx=urx);
    else:
        rx = r"^ *\( *(?:{urx} *, *){{{rep1}}}{urx} *,? *\) *$".format(
            rep1=length-1,
            urx=urx);
    return re.match(rx,s);

def evalt(s):
    '''a "save" eval for a tuple by adding a comma to the end'''
    return eval(re.sub("(\) *$)",",\g<1>",s));

def parse_numtuple(s,intype,length=2,scale=1):
    '''parse a string into a list of numbers of a type'''
    if intype == int:
        numrx = intrx_s;
    elif intype == float:
        numrx = fltrx_s;
    else:
        raise NotImplementedError("Not implemented for type: {}".format(
            intype));
    if parse_utuple(s, numrx, length=length) is None:
        raise ValueError("{} is not a valid number tuple.".format(s));
    return [x*scale for x in evalt(s)];

def quote_subs(s, rx=isrx, colorfix=False):
    if colorfix:
        if type(rx) != str:
            rx = rx.pattern;
        return re.sub("(\(|,) *({})".format(rx), '\g<1> "\g<2>"', s);
    return re.sub(rx,'"\g<0>"',s);

def parse_ctuple(s,length=2):
    '''parse a string of acceptable colors into matplotlib, that is, either
       strings, or three tuples of rgb. Don't quote strings.
    '''
    if parse_utuple(s, colrx_s, length=length) is None:
        raise ValueError("{} is not a valid color tuple.".format(s));
    #quote strings
    s=quote_subs(s,colorfix=True);
    return evalt(s);

def parse_stuple(s,length=2):
    '''parse a string of identifier strings, must start with alpha or underscore.
       Don't quote strings'''
    if parse_utuple(s, isrx_s, length=length) is None:
        raise ValueError("{} is not a valid string tuple.".format(s));
    s = quote_subs(s);
    return evalt(s);

def parse_ftuple(s,length=2,scale=1):
    '''parse a string into a list of floats'''
    return parse_numtuple(s,float,length,scale);

def parse_ituple(s,length=2,scale=1):
    '''parse a string into a list of floats'''
    return parse_numtuple(s,int,length,scale);

def parse_colors(s, length=1):
    '''helper for parsing a string that can be either a matplotlib
       color or be a tuple of colors. Returns a tuple of them either
       way.
    '''
    if length and length > 1:
        return parse_ctuple(s,length=length);
    if re.match('^ *{} *$'.format(isrx_s), s):
        #it's just a string.
        return [s];
    elif re.match('^ *{} *$'.format(rgbrx_s), s):
        return [eval(s)];
    else:
        return parse_ctuple(s,length=length);

def parse_qs(s, rx, parsef=None, length=2, quote=False):
    '''helper for parsing a string that can both rx or parsef
       which is obstensibly the parsef for rx.

       Use parse colors for color tuples. This won't work with
       those.
    '''
    if type(rx) != str:
        rx = rx.pattern;
    if re.match(" *\(.*\)", s):
        if not parsef:
            if parse_utuple(s,rx,length=length):
                if quote:
                    s=quote_subs(s);
                return evalt(s);
            else:
                raise ValueError("{} did is not a valid tuple of {}".format(
                    s, rx));
        else:
            return parsef(s,length=length);
    elif re.match('^ *{} *$'.format(rx), s):
        if quote:
            return eval('["{}"]'.format(s));
        return eval('[{}]'.format(s));
    else:
        raise ValueError("{} does not match '{}' or the passed parsef".format(
            s,rx));
    

def sd(d,**kw):
    '''
    A hack to return a modified dict dynamically. Basically,
    Does "classless OOP" as in js but with dicts, although
    not really for the "verb" parts of OOP but more of the
    "subject" stuff.

    Confused? Here's how it works:

    `d` is a dict. We have that

    sd(d, perfect=42, gf='qt3.14')

    returns a dict like d but with d['perfect']==42 and
    d['gf']=='qt3.14'. 'sd' stands for "setdefault" which is,
    you know, what we do when we set elements of a dict.
    
    I plan to  use this heavily.
    '''
    #HURR SO COMPLICATED
    r={};        #copy. if you want to modify,
    r.update(d); #use {}.update
    r.update(kw);
    return r;

def savetxt(fname, s="",bin=False):
    '''write to a text file'''
    mode = 'wb' if bin else 'w'
    with open(fname,mode) as f:
        f.write(s);

def readtxt(fname,bin=False):
    '''read a text file'''
    mode = 'rb' if bin else 'r'
    with open(fname,mode) as f:
        s = f.read();
    return s;

def take(d,*l):
    '''take a list of keys from a dict'''
    if type(l[0]) is not str:
        l = l[0];
    return {i:d[i] for i in l};

def destr(d,*l):
    '''destructure a dict (like take, but return a list)'''
    if type(l[0]) is not str:
        l=l[0];
    return [d[i] for i in l];

def takef(d,*l,val=None):
    '''take(f) a list of keys and fill in others with val'''
    if type(l[0]) is not str:
        l=l[0];    
    return {i:(d[i] if i in d else val)
            for i in l};

def stridesf(l,N,fill=[]):
    '''
    return list `l` divided into `N` parts by striding. If `N` exceeds
    len(l), then return `fill` for each extra slot.

    basically,
        stridesf([1,2,3,4],2)   -> [[1,3],[2,4]]
        stridesf([1,2,3,4],5)   -> [[1],[2],[3],[4],[]]
        stridesf(
            [1,2,3,4],5,fill='wowza')  -> [[1],[2],[3],[4],'wowza']
    '''
    if len(l) < N:
        l = [[i] for i in l] +  [fill]*(N-len(l));
    else:
        l = [ l[i::N] for i in range(N) ];
    return l;


def mk_getkw(kw, defaults,prefer_passed=False):
    '''
    a helper for generating a function for reading keywords in
    interface functions with a dictionary with defaults

    expects the defaults dictionary to have keywords you request.

    example:
    defaults = dict(a='a',b=3);
    def bigfunc(**kw):
        getkw=mk_getkw(kw,defaults);

        # I want the callers' `a', or the default if they don't
        # supply it
        a=getkw('a');
        c = [a]*getkw('b');
        return c,c[0]; 

    Option:
        prefer_passed -- use "l in kw" only, not test.
    '''
    def getkw(*ls):
        r = [ kw[l] if test(kw,l) else defaults[l]
              for l in ls ];
        if len(r) == 1: return r[0];
        return r;
    def getkw_prefer_passed(*ls):
        r = [ kw[l] if l in kw else defaults[l]
              for l in ls ];
        if len(r) == 1: return r[0];
        return r;
    return getkw if not prefer_passed else getkw_prefer_passed;

            

from time import perf_counter;
class TimestampVprinter():
    '''
    vprinter with a timestamp
    
    '''
    def __init__(self, preamble='',tabnum=2,timefmt='{:06.2f}'):
        self.pref = '{}{}:\n{}'.format(preamble,timefmt,' '*tabnum);
        self.starttime = perf_counter();
    def __call__(self, *arg):
        print(self.pref.format(perf_counter() - self.starttime),*arg);

def autovp(*arg):
    '''
    make a vprinter with the preamble of exectable name.
    '''
    import sys;
    preamble=' '.join((sys.argv[0],)+arg)+' '
    return TimestampVprinter(preamble=preamble);

def novp(*avg):
    ''' what do you think '''
    pass;

def choose_autovp(choose, *avg):
    '''call autovp based on choose'''
    if choose: return autovp(*avg);
    return novp;

def sdl(l,**kw):
    '''apply sd to a list l of dictionaries'''
    return [sd(i,**kw) for i in l];
