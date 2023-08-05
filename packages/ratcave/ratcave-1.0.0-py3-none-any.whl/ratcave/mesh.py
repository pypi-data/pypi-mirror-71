"""
This module contains the Mesh and EmptyEntity classes.
"""

import pickle
import numpy as np
from .utils import NameLabelMixin
from . import physical, shader, gl
from .texture import Texture
from .vertex import VertexArray, pairwise
from copy import deepcopy


def calculate_normals(vertices):
    """Return Nx3 normal array from Nx3 vertex array."""
    verts = np.array(vertices, dtype=float)
    normals = np.zeros_like(verts)
    for start, end in pairwise(np.arange(0, verts.shape[0] + 1, 3)):
        vecs = np.vstack((verts[start + 1] - verts[start], verts[start + 2] - verts[start]))  # Get triangle of vertices and calculate 2-1 and 3-1
        vecs /= np.linalg.norm(vecs, axis=1, keepdims=True)  # normalize vectors
        normal = np.cross(*vecs)  # normal is the cross products of vectors.
        normals[start:end, :] = normal / np.linalg.norm(normal)
    return normals


def gen_fullscreen_quad(name='FullScreenQuad'):
    verts = np.array([[-1, -1, -.5], [-1, 1, -.5], [1, 1, -.5], [-1, -1, -.5], [1, 1, -.5], [1, -1, -.5]],
                     dtype=np.float32)
    normals = np.array([[0, 0, 1]] * 6, dtype=np.float32)
    texcoords = np.array([[0, 0], [0, 1], [1, 1], [0, 0], [1, 1], [1, 0]], dtype=np.float32)
    return Mesh(name=name, arrays=(verts, normals, texcoords), mean_center=False)


class EmptyEntity(shader.HasUniformsUpdater, physical.PhysicalGraph, NameLabelMixin):
    """Returns an EmptyEntity object that occupies physical space and uniforms, but doesn't draw anything when draw() is called."""

    def draw(self, *args, **kwargs):
        """Passes all given arguments"""
        pass

    def reset_uniforms(self):
        """Passes alll given arguments"""
        pass


class Mesh(shader.HasUniformsUpdater, physical.PhysicalGraph, NameLabelMixin, VertexArray):

    def __init__(self, arrays, textures=(), mean_center=True,
                 gl_states=(), point_size=15, visible=True, **kwargs):
        """
        Returns a Mesh object, containing the position, rotation, and color info of an OpenGL Mesh.

        Meshes have two coordinate system, the "local" and "world" systems, on which the transforms are performed
        sequentially.  This allows them to be placed in the scene while maintaining a relative position to one another.

        .. note:: Meshes are not usually instantiated directly, but from a 3D file, like the WavefrontReader .obj and .mtl files.

        Args:
            arrays (tuple): a list of 2D arrays to be rendered.  All arrays should have same number of rows. Arrays will be accessible in shader in same attrib location order.
            mean_center (bool):
            texture (Texture): a Texture instance, which is linked when the Mesh is rendered.
            gl_states:
            drawmode: specifies the OpenGL draw mode
            point_size (int):
            visible (bool): whether the Mesh is available to be rendered.  To make hidden (invisible), set to False.

        Returns:
            Mesh instance
        """
        super(Mesh, self).__init__(arrays=arrays, **kwargs)
        self.reset_uniforms()

        # Mean-center vertices and move position to vertex mean.
        vertex_mean = self.vertices.mean(axis=0) #if not self.indices is None else self.vertices[self.indices, :].mean(axis=0)

        if mean_center:
            self.arrays[0] -= vertex_mean
        if 'position' in kwargs:
            self.position.xyz = kwargs['position']
        elif mean_center:
            self.position.xyz = vertex_mean
        self._mean_center = mean_center
        # self.position.xyz = vertex_mean if not 'position' in kwargs else kwargs['position']

        self.textures = list(textures)
        self.gl_states = gl_states
        self.point_size = point_size
        self.visible = visible

    def __repr__(self):
        return "<Mesh(name='{self.name}', position_rel={self.position}, position_glob={self.position_global}, rotation={self.rotation})".format(
            self=self)

    def copy(self):
        """Returns a copy of the Mesh."""
        return Mesh(arrays=deepcopy([arr.copy() for arr in [self.vertices, self.normals, self.texcoords]]),
                    textures=self.textures, mean_center=deepcopy(self._mean_center),
                    position=self.position.xyz, rotation=self.rotation.__class__(*self.rotation[:]),
                    scale=self.scale.xyz,
                    drawmode=self.drawmode, point_size=self.point_size, visible=self.visible,
                    gl_states=deepcopy(self.gl_states))

    def to_pickle(self, filename):
        """Save Mesh to a pickle file, given a filename."""
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def from_pickle(cls, filename):
        """Loads and Returns a Mesh from a pickle file, given a filename."""
        with open(filename, 'rb') as f:
            mesh = pickle.load(f)
            mesh2 = mesh.copy()
        return mesh2

    @classmethod
    def from_primitive(cls, name, position=(0, 0, 0), **kwargs):
        """Returns a Mesh from the obj_primtives.obj file."""
        from .wavefront import WavefrontReader
        from .resources import obj_primitives
        reader = WavefrontReader(obj_primitives)
        mesh = reader.get_mesh(name, position=position, **kwargs)
        return mesh

    def reset_uniforms(self):
        """ Resets the uniforms to the Mesh object to the ""global"" coordinate system"""
        self.uniforms['model_matrix'] = self.model_matrix_global.view()
        self.uniforms['normal_matrix'] = self.normal_matrix_global.view()

    @property
    def vertices(self):
        """Mesh vertices, centered around 0,0,0."""
        return self.arrays[0].view()

    @vertices.setter
    def vertices(self, value):
        self.arrays[0] = value

    @property
    def normals(self):
        """Mesh normals array."""
        return self.arrays[1].view()

    @normals.setter
    def normals(self, value):
        self.arrays[1] = value

    @property
    def texcoords(self):
        """UV coordinates"""
        return self.arrays[2].view()

    @texcoords.setter
    def texcoords(self, value):
        self.arrays[2] = value

    @property
    def vertices_local(self):
        """Vertex position, in local coordinate space (modified by model_matrix)"""
        return np.dot(self.model_matrix, np.append(self.vertices, np.ones(self.vertices.shape[0], 1), axis=1))[:3]

    @property
    def vertices_global(self):
        """Vertex position, in world coordinate space (modified by model_matrix)"""
        return np.dot(self.model_matrix_global, np.append(self.vertices, np.ones(self.vertices.shape[0], 1), axis=1))[:3]

    @classmethod
    def from_incomplete_data(cls, vertices, normals=(), texcoords=(), **kwargs):
        """Return a Mesh with (vertices, normals, texcoords) as arrays, in that order.
           Useful for when you want a standardized array location format across different amounts of info in each mesh."""
        normals = normals if hasattr(texcoords, '__iter__') and len(normals) else calculate_normals(vertices)
        texcoords = texcoords if hasattr(texcoords, '__iter__') and len(texcoords) else np.zeros((vertices.shape[0], 2),
                                                                                                 dtype=np.float32)
        return cls(arrays=(vertices, normals, texcoords), **kwargs)

    def draw(self):
        """ Draw the Mesh if it's visible, from the perspective of the camera and lit by the light. The function sends the uniforms"""
        if not self._loaded:
            self.load_vertex_array()

        if self.visible:
            if self.drawmode == gl.GL_POINTS:
                gl.glPointSize(self.point_size)

            for texture in self.textures:
                texture.bind()

            self.uniforms.send()
            super(Mesh, self).draw()

            for texture in self.textures:
                texture.unbind()

    @property
    def collider(self):
        return self._collider

    @collider.setter
    def collider(self, value):
        from .collision import ColliderBase
        if not isinstance(value, ColliderBase):
            raise TypeError("collider must inherit from ColliderBase.")
        self._collider = value
        self._collider.parent = self