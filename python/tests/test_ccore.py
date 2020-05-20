import array
import pickle

import numpy as np
import pytest

from mspasspy.ccore import (dmatrix,
                            Metadata,
                            Seismogram,
                            TimeSeries)

def setup_function(function):
    pass

def test_dmatrix():
    dm = dmatrix()
    assert dm.rows() == 0

    dm = dmatrix(9,4)
    assert dm.rows() == 9
    assert dm.columns() == 4

    md = [array.array('l', (0 for _ in range(5))) for _ in range(3)]
    for i in range(3):
        for j in range(5):
            md[i][j] = i*5+j
    dm = dmatrix(md)
    assert np.equal(dm,md).all()

    dm_c = dmatrix(dm)
    assert (dm_c[:] == dm).all()

    dm_c.zero()
    assert not dm_c[:].any()

    md = np.zeros((7,4), dtype=np.double, order='F')
    for i in range(7):
        for j in range(4):
            md[i][j] = i*4+j
    dm = dmatrix(md)
    assert (dm == md).all()

    dm_c = dmatrix(dm)
    dm += dm_c
    assert (dm == md+md).all()
    dm += md
    assert (dm == md+md+md).all()
    assert type(dm) == dmatrix
    dm -= dm_c
    dm -= dm_c
    dm -= md
    assert not dm[:].any()
    assert type(dm) == dmatrix

    dm_c = dmatrix(dm)
    
    md = np.zeros((7,4), dtype=np.single, order='C')
    for i in range(7):
        for j in range(4):
            md[i][j] = i*4+j
    dm = dmatrix(md)
    assert (dm == md).all()

    md = np.zeros((7,4), dtype=np.int, order='F')
    for i in range(7):
        for j in range(4):
            md[i][j] = i*4+j
    dm = dmatrix(md)
    assert (dm == md).all()

    md = np.zeros((7,4), dtype=np.unicode_, order='C')
    for i in range(7):
        for j in range(4):
            md[i][j] = i*4+j
    dm = dmatrix(md)
    assert (dm == np.float_(md)).all()

    md = np.zeros((53,37), dtype=np.double, order='C')
    for i in range(53):
        for j in range(37):
            md[i][j] = i*37+j
    dm = dmatrix(md)
    
    assert dm[17, 23] == md[17, 23]
    assert (dm[17] == md[17]).all()
    assert (dm[::] == md[::]).all()
    assert (dm[3::] == md[3::]).all()
    assert (dm[:5:] == md[:5:]).all()
    assert (dm[::7] == md[::7]).all()
    assert (dm[-3::] == md[-3::]).all()
    assert (dm[:-5:] == md[:-5:]).all()
    assert (dm[::-7] == md[::-7]).all()
    assert (dm[11:41:7] == md[11:41:7]).all()
    assert (dm[-11:-41:-7] == md[-11:-41:-7]).all()
    assert (dm[3::, 13] == md[3::, 13]).all()
    assert (dm[19, :5:] == md[19, :5:]).all()
    assert (dm[::-7,::-11] == md[::-7,::-11]).all()

    with pytest.raises(IndexError, match = 'out of bounds for dmatrix'):
        dummy = dm[3,50]
    with pytest.raises(IndexError, match = 'out of bounds for axis 1'):
        dummy = dm[80]
    
    with pytest.raises(IndexError, match = 'out of bounds for dmatrix'):
        dm[3,50] = 1.0
    with pytest.raises(IndexError, match = 'out of bounds for axis 0'):
        dm[60,50] = 1

    dm[7,17] = 3.14
    assert dm[7,17] == 3.14

    dm[7,17] = '6.28'
    assert dm[7,17] == 6.28

    dm[7] = 10
    assert (dm[7] == 10).all()

    dm[::] = md
    assert (dm == md).all()

    dm[:,-7] = 3.14
    assert (dm[:,-7] == 3.14).all()

    dm[17,:] = 3.14
    assert (dm[17,:] == 3.14).all()

    dm[3:7,-19:-12] = 3.14
    assert (dm[3:7,-19:-12] == 3.14).all()


def test_Metadata():
    md = Metadata()
    assert repr(md) == 'Metadata({})'
    dic = {1:1}
    md.put('dict', dic)
    val = md.get('dict')
    val[2] = 2
    del val
    dic[3] = 3
    del dic
    md['dict'][4] = 4
    assert md['dict'] == {1: 1, 2: 2, 3: 3, 4: 4}

    md = Metadata({'array': np.array([3, 4])})
    md['dict']      = {1: 1, 2: 2}
    md['str\'i"ng'] = 'str\'i"ng'
    md["str'ing"]   = "str'ing"
    md['double']    = 3.14
    md['bool']      = True
    md['int']       = 7
    md["string"]    = "str\0ing"
    md["string"]    = "str\ning"
    md["str\ting"]  = "str\ting"
    md["str\0ing"]  = "str\0ing"
    md["str\\0ing"] = "str\\0ing"
    md_copy = pickle.loads(pickle.dumps(md))
    for i in md:
        if i == 'array':
            assert (md[i] == md_copy[i]).all()
        else:
            assert md[i] == md_copy[i]
    assert md[i] == md_copy[i]

    md = Metadata({
        "<class 'numpy.ndarray'>": np.array([3, 4]),
        "<class 'dict'>"         : {1: 1, 2: 2},
        'string'                 : 'string',
        'double'                 : 3.14,
        'bool'                   : True,
        'long'                   : 7,
        "<class 'bytes'>"        : b'\xba\xd0\xba\xd0',
        "<class 'NoneType'>"     : None })
    for i in md: 
        assert md.type(i) == i
    
    md[b'\xba\xd0']= b'\xba\xd0'
    md_copy = pickle.loads(pickle.dumps(md))
    for i in md:
        if i == "<class 'numpy.ndarray'>":
            assert (md[i] == md_copy[i]).all()
        else:
            assert md[i] == md_copy[i]

    del md["<class 'numpy.ndarray'>"]
    md_copy.clear("<class 'numpy.ndarray'>")
    assert not "<class 'numpy.ndarray'>" in md
    assert not "<class 'numpy.ndarray'>" in md_copy
    assert md.keys() == md_copy.keys()

    with pytest.raises(TypeError, match = 'mspass::Metadata'):
        reversed(md)
    
    md = Metadata({1:1,3:3})
    md_copy = Metadata({2:2,3:30})
    md += md_copy
    assert md.__repr__() == "Metadata({'1': 1, '2': 2, '3': 30})"
