import Part


def is_edge_parallel_to_x_axis(edge: Part.Edge) -> bool:
    """Check if the given edge is parallel to the X axis.

    :param edge: Edge to check if it's parallel to the X axis.
    :type edge: Part.Edge
    :return: ``True`` if parallel to the X axis, ``False`` otherwise.
    :rtype: bool
    """
    return _is_edge_parallel_to_axis(edge, 'x')


def is_edge_parallel_to_y_axis(edge: Part.Edge) -> bool:
    """Check if the given edge is parallel to the Y axis.

    :param edge: Edge to check if it's parallel to the Y axis.
    :type edge: Part.Edge
    :return: ``True`` if parallel to the Y axis, ``False`` otherwise.
    :rtype: bool
    """
    return _is_edge_parallel_to_axis(edge, 'y')


def is_edge_parallel_to_z_axis(edge: Part.Edge) -> bool:
    """Check if the given edge is parallel to the Z axis.

    :param edge: Edge to check if it's parallel to the Z axis.
    :type edge: Part.Edge
    :return: ``True`` if parallel to the Z axis, ``False`` otherwise.
    :rtype: bool
    """
    return _is_edge_parallel_to_axis(edge, 'z')


def _is_edge_parallel_to_axis(edge, axis):
    index_by_axis = {'x': 0, 'y': 1, 'z': 2}
    inverse_orientations = filter(
        lambda item: item[0] != axis, index_by_axis.items())
    a_index, b_index = map(lambda item: item[1], inverse_orientations)
    first_point = edge.valueAt(edge.FirstParameter)
    a1 = round(first_point[a_index])
    b1 = round(first_point[b_index])

    last_point = edge.valueAt(edge.LastParameter)
    a2 = round(last_point[a_index])
    b2 = round(last_point[b_index])

    return a1 == a2 and b1 == b2
