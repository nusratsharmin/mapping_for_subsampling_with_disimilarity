import numpy as np
import nibabel as nib
from dipy.tracking import utils


def _mapping_to_voxel(affine, voxel_size):
    """Inverts affine and returns a mapping so voxel coordinates. This
    function is an implementation detail and only meant to be used with
    ``_to_voxel_coordinates``.

    Parameters
    ----------
    affine : array_like (4, 4)
        The mapping from voxel indices, [i, j, k], to real world coordinates.
        The inverse of this mapping is used unless `affine` is None.
    voxel_size : array_like (3,)
        Used to support deprecated trackvis space.

    Return
    ------
    lin_T : array (3, 3)
        Transpose of the linear part of the mapping to voxel space, (ie
        ``inv(affine)[:3, :3].T``)
    offset : array or scaler
        Offset part of the mapping (ie, ``inv(affine)[:3, 3]``) + ``.5``. The
        half voxel shift is so that truncating the result of this mapping
        will give the correct integer voxel coordinate.

    Raises
    ------
    ValueError
        If both affine and voxel_size are None.

    """
    if affine is not None:
        affine = np.array(affine, dtype=float)
        inv_affine = np.linalg.inv(affine)
        lin_T = inv_affine[:3, :3].T.copy()
        offset = inv_affine[:3, 3] + .5
    elif voxel_size is not None:
        _voxel_size_deprecated()
        voxel_size = np.asarray(voxel_size, dtype=float)
        lin_T = np.diag(1. / voxel_size)
        offset = 0.
    else:
        raise ValueError("no affine specified")
    return lin_T, offset


def _to_voxel_coordinates(streamline, lin_T, offset):
    """Applies a mapping from streamline coordinates to voxel_coordinates,
    raises an error for negative voxel values."""
    inds = np.dot(streamline, lin_T)
    inds += offset
    if inds.min() < 0:
        raise IndexError('streamline has points that map to negative voxel'
                         ' indices')
    return inds.astype(int)

def streamline_mapping_new_step(streamlines, voxel_size=None, affine=None,
                       mapping_as_streamlines=False):
    """
    This function is for checking the crossing of the streamline( That means if any streamline has the same voxel"
    This function are same as dipy but with some modification
    """
    

    lin, offset = _mapping_to_voxel(affine, voxel_size)
    if mapping_as_streamlines:
        streamlines = list(streamlines)
    mapping = {}
    mapping_filter={}
    idx=[]
    for i, sl in enumerate(streamlines):
        voxel_indices = _to_voxel_coordinates(sl, lin, offset)
        flag=0
        # Get the unique voxels every streamline passes though
        uniq_points = set()
        for j in range(voxel_indices.shape[0]):
            point = (voxel_indices[j, 0],
                     voxel_indices[j, 1],
                     voxel_indices[j, 2])
            uniq_points.add(point)

        # Add the index of this streamline for each uniq voxel
        for point in uniq_points:
           if point in mapping:
              flag=0
              break
           else:
             mapping[point] = [i]
             flag=1
        #Add the ids of streamline which has no crossing
        if flag==1: 
             i=np.array([i])
             idx.extend(i)

    # If mapping_as_streamlines replace ids with streamlines
    if mapping_as_streamlines:
        for key in mapping:
            mapping[key] = [streamlines[i] for i in mapping[key]]

    return idx

