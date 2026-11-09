"""Pythia to HepMC3 with explicit vertices and named LHE weights."""
import numpy as np
import pyhepmc


def to_hepmc(pythia, number, weights, run_info):
    particles = list(pythia.event)[1:]
    values = lambda name: np.array([getattr(p, name)() for p in particles])
    event = pyhepmc.GenEvent(pyhepmc.Units.GEV, pyhepmc.Units.MM)
    event.from_hepevt(
        number, values('px'), values('py'), values('pz'), values('e'),
        values('m'), values('id'), values('statusHepMC'),
        parents=np.array([[p.mother1(), p.mother2()] for p in particles]),
        vx=values('xProd'), vy=values('yProd'), vz=values('zProd'), vt=values('tProd'))
    for vertex in list(event.vertices):
        if not vertex.particles_out:
            for particle in list(vertex.particles_in):
                vertex.remove_particle_in(particle)
            event.remove_vertex(vertex)
    for vertex in list(event.vertices):
        if not vertex.particles_in:
            for particle in list(vertex.particles_out):
                vertex.remove_particle_out(particle)
            event.remove_vertex(vertex)
        else:
            vertex.status = 1
    original = [p for p in particles if p.isFinal()]
    stored = [p for p in event.particles if p.status == 1]
    if len(original) != len(stored):
        raise ValueError('Stable-particle count changed in HepMC conversion.')
    # Match every final particle's identity and four-momentum in stored order.
    for before, after in zip(original, stored):
        a = [before.px(), before.py(), before.pz(), before.e()]
        b = [after.momentum.px, after.momentum.py, after.momentum.pz, after.momentum.e]
        if before.id() != after.pid or not np.allclose(a, b, rtol=0, atol=1e-8):
            raise ValueError('Stable-particle identity or momentum changed in conversion.')
    event.run_info = run_info
    event.weights = [weights[name] for name in run_info.weight_names]
    info = pythia.infoPython()
    event.attributes['signal_process_id'] = int(info.code())
    event.attributes['mpi'] = int(info.nMPI())
    event.attributes['event_scale'] = float(info.QRen())
    cross_section = pyhepmc.GenCrossSection()
    cross_section.set_cross_section(info.sigmaGen() * 1e9, info.sigmaErr() * 1e9)
    event.cross_section = cross_section
    return event
