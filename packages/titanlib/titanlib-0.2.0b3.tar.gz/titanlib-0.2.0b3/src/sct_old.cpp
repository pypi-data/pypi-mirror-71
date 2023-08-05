#include <vector>
#include <math.h>
#include "titanlib.h"
#include <assert.h>
#include <iostream>
#include <exception>
extern "C" {
#include "sct_smart_boxes.h"
}

ivec titanlib::sct_old(const vec& lats,
        const vec& lons,
        const vec& elevs,
        const vec& values,
        int nmin,
        int nmax,
        int nminprof,
        float min_elev_diff,
        float dhmin,
        float dz,
        const vec& t2pos,
        const vec& t2neg,
        const vec& eps2,
        vec& prob_gross_error,
        vec& rep,
        ivec& boxids) {

    // Check inputs
    int N = lats.size();
    if(nmin == 0 || nmax == 0)
        throw std::runtime_error("nmin and nmax must be > 0");
    if(lons.size() != N || elevs.size() != N || values.size() != N)
        throw std::invalid_argument("Input dimension mismatch");
    vec x, y;
    titanlib::util::convert_to_proj(lats, lons, "+proj=lcc +lat_0=63 +lon_0=15 +lat_1=63 +lat_2=63 +no_defs +R=6.371e+06", x, y);

    dvec dx(x.begin(), x.end());
    dvec dy(y.begin(), y.end());

    dvec delevs(elevs.begin(), elevs.end());
    dvec dvalues(values.begin(), values.end());
    dvec dt2pos(t2pos.begin(), t2pos.end());
    dvec dt2neg(t2neg.begin(), t2neg.end());
    dvec deps2(eps2.begin(), eps2.end());

    double dmin_elev_diff = min_elev_diff;
    double ddhmin = dhmin;
    double ddz = dz;
    // int nmax = 200;
    // int nmin = 50;
    // int nminprof = 10;
    // double min_elev_diff = 100;
    // double dhmin = 10000;
    // double dz = 30;
    dvec dsct;
    dvec drep;
    boxids.resize(N, 0);
    ivec flags(N, 0);
    dsct.resize(N, 0);
    drep.resize(N, 0);

    sct_smart_boxes(&N, &dx[0], &dy[0], &delevs[0], &dvalues[0], &nmax, &nmin, &nminprof, &dmin_elev_diff, &ddhmin, &ddz, &dt2pos[0], &dt2neg[0], &deps2[0], &flags[0], &dsct[0], &drep[0], &boxids[0]);
    prob_gross_error = vec(dsct.begin(), dsct.end());
    rep = vec(drep.begin(), drep.end());

    return flags;
}
