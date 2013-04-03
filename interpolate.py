import numpy as np

try:
    from mdtraj import trajectory
except ImportError:
    print 'Download and install the mdtraj package from'
    print 'https://github.com/rmcgibbo/mdtraj'
    raise

try:
    from nebterpolator.mpiutils import mpi_root
    from nebterpolator.io import XYZFile
    from nebterpolator.path_operations import smooth_internal, smooth_cartesian
except ImportError:
    print 'Download and install the nebterpolator package from'
    print 'https://github.com/rmcgibbo/nebterpolator'
    raise


traj = trajectory.load_dcd('pulling.dcd', 'input.pdb')
atom_names = [a.element.symbol for a in traj.topology.atoms()]

traj.xyz = smooth_cartesian(traj.xyz, strength=150)
for i in range(traj.n_frames):
    traj._xyz[i] -= np.mean(traj._xyz[i], axis=0)

traj.xyz = traj.xyz[::10]
print 'Saving to disk'
traj.save_dcd('smoothed.dcd', force_overwrite=True)
