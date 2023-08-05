
cdef extern from "snp_hwe.h" namespace 'snphwe':
    double SNPHWE(long, long, long) except +ValueError

def snphwe(obs_hets, obs_hom1, obs_hom2):
    return SNPHWE(round(obs_hets), round(obs_hom1), round(obs_hom2))
