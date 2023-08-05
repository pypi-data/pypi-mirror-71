from .workflow import Workflow
from .job import Job


def compute(
    obj,
    geoctx=None,
    format="pyarrow",
    destination="download",
    file=None,
    timeout=None,
    block=True,
    progress_bar=None,
    client=None,
    cache=True,
    **params
):
    """
    Compute a proxy object and wait for its result.

    Parameters
    ----------
    obj: Proxytype
        A proxy object to compute.
    geoctx: `~.workflows.types.geospatial.GeoContext`, or None
        The GeoContext parameter under which to run the computation.
        Almost all computations will require a `~.workflows.types.geospatial.GeoContext`,
        but for operations that only involve non-geospatial types,
        this parameter is optional.
    format: str or dict, default "pyarrow"
        The serialization format for the result.
        See the `formats
        <https://docs.descarteslabs.com/descarteslabs/workflows/docs/formats.html#output-formats>`_
        documentation for more information.
        If "pyarrow" (the default), returns an appropriate Python object, otherwise returns raw bytes.
    destination: str or dict, default "download"
        The destination for the result.
        See the `destinations
        <https://docs.descarteslabs.com/descarteslabs/workflows/docs/destinations.html#output-destinations>`_
        documentation for more information.
    file: path or file-like object, optional
        If specified, writes results to the path or file instead of returning them.
    timeout: int, optional
        The number of seconds to wait for the result, if ``block`` is True.
        Raises ``JobTimeoutError`` if the timeout passes.
    block: bool, default True
        If True (default), block until the job is completed,
        or ``timeout`` has passed.
        If False, immediately returns a `Job` (which has already had `~Job.execute` called).
    progress_bar: bool, default None
        Whether to draw the progress bar. If ``None`` (default),
        will display a progress bar in Jupyter Notebooks, but not elsewhere.
        Ignored if ``block==False``.
    client: `.workflows.client.Client`, optional
        Allows you to use a specific client instance with non-default
        auth and parameters
    cache: bool, default True
        Whether to use the cache for this job.
    **params: Proxytype
        Parameters under which to run the computation, such as ``geoctx``.

    Returns
    -------
    result: Python object, bytes, or None
        When ``format="pyarrow"`` (the default), returns an appropriate Python object representing
        the result, either as a plain Python type, or object from `descarteslabs.workflows.result_types`.
        For other formats, returns raw bytes. Consider using `file` in that case to save the results to a file.
        If the destination doesn't support retrieving results (like "email"), returns None

    Example
    -------
    >>> import descarteslabs.workflows as wf
    >>> num = wf.Int(1) + 1
    >>> wf.compute(num) # doctest: +SKIP
    2
    >>> # same computation but do not block
    >>> job = wf.compute(num, block=False) # doctest: +SKIP
    >>> job # doctest: +SKIP
    <descarteslabs.workflows.models.job.Job object at 0x...>
    >>> job.result() # doctest: +SKIP
    2
    >>> # pass multiple proxy objects to `wf.compute` to compute all at once
    >>> wf.compute((num, num, num)) # doctest: +SKIP
    (2, 2, 2)

    >>> # specifying a format
    >>> img = wf.Image.from_id("sentinel-2:L1C:2019-05-04_13SDV_99_S2B_v1").pick_bands("red")
    >>> wf.compute(img, geoctx=ctx, format="pyarrow") # default # doctest: +SKIP
    ImageResult:
    ...
    >>> # same computation but with json format
    >>> wf.compute(img, geoctx=ctx, format="json") # doctest: +SKIP
    b'{"ndarray":[[[0.39380000000000004,0.3982,0.3864,...
    >>> # same computation but with geotiff format (and some format options)
    >>> bytes_ = wf.compute(img, geoctx=ctx, format={"type": "geotiff", "tiled": False}) # doctest: +SKIP
    >>> # you probably want to save the geotiff to a file:
    >>> wf.compute(img, geoctx=ctx, file="my_geotiff.tif", format={"type": "geotiff", "tiled": False}) # doctest: +SKIP

    >>> # specifying a destination
    >>> num = wf.Int(1) + 1
    >>> wf.compute(num, destination="download") # default # doctest: +SKIP
    2
    >>> # same computation but with email destination
    >>> wf.compute(num, destination="email") # doctest: +SKIP
    >>> # now with some destination options
    >>> wf.compute(
    ...     num,
    ...     destination={
    ...         "type": "email",
    ...         "subject": "My Computation is Done"
    ...     },
    ...     format="json",
    ... ) # doctest: +SKIP
    """
    if geoctx is not None:
        params["geoctx"] = geoctx

    job = Job(
        obj, params, format=format, destination=destination, client=client, cache=cache
    )
    if block:
        job.wait(timeout=timeout, progress_bar=progress_bar)
        if file is not None:
            return job.result_to_file(file)
        else:
            try:
                return job.result()
            except NotImplementedError:
                # suppress error if destination isn't supported; return nothing
                return
    else:
        return job


def publish(obj, name="", description="", client=None):
    """
    Publish a proxy object as a `Workflow`.

    Parameters
    ----------
    obj: Proxytype
        A proxy object to compute
    name: str, default ""
        Name for the new `Workflow`
    description: str, default ""
        Long-form description of this `Workflow`. Markdown is supported.
    client: `.workflows.client.Client`, optional
        Allows you to use a specific client instance with non-default
        auth and parameters

    Returns
    -------
    workflow: `Workflow`
        The saved `Workflow` object. ``workflow.id`` contains the ID of the new Workflow.

    Example
    -------
    >>> from descarteslabs.workflows import Image, Function
    >>> def ndvi(img):
    ...     nir, red = img.unpack_bands("nir red")
    ...     return (nir - red) / (nir + red)
    >>> func = Function.from_callable(ndvi, Image)
    >>> workflow = func.publish("NDVI") # doctest: +SKIP
    >>> workflow # doctest: +SKIP
    <descarteslabs.workflows.models.workflow.Workflow object at 0x...>
    """
    workflow = Workflow.build(obj, name=name, description=description, client=client)
    workflow.save()
    return workflow


def retrieve(workflow_id, client=None):
    """
    Load a published `Workflow` object.

    Parameters
    ----------
    workflow_id: str
        ID of the `Workflow` to retrieve
    client: Compute, optional
        Allows you to use a specific client instance with non-default
        auth and parameters

    Returns
    -------
    workflow: `Workflow`
        Object representing the workflow, including both its metadata
        (like ``workflow.name``, ``workflow.description``) and proxy object
        (``workflow.object``).

    Example
    -------
    >>> from descarteslabs.workflows import Image, Function, retrieve
    >>> def ndvi(img):
    ...     nir, red = img.unpack_bands("nir red")
    ...     return (nir - red) / (nir + red)
    >>> func = Function.from_callable(ndvi, Image) # create a function that can be called on an Image
    >>> workflow = func.publish("NDVI") # doctest: +SKIP
    >>> workflow.id # doctest: +SKIP
    '42cea96a864811f00f0bcdb8177ba80d6dc9c7492e13e794'
    >>> same_workflow = retrieve('42cea96a864811f00f0bcdb8177ba80d6dc9c7492e13e794') # doctest: +SKIP
    >>> same_workflow # doctest: +SKIP
    <descarteslabs.workflows.models.workflow.Workflow object at 0x...>
    >>> img = Image.from_id("sentinel-2:L1C:2019-05-04_13SDV_99_S2B_v1")
    >>> same_workflow.object(img).compute(geoctx) # geoctx is an arbitrary geocontext for 'img' # doctest: +SKIP
    >>> # notice the bandname is comprised of the operations called to create it
    ImageResult:
      * ndarray: MaskedArray<shape=(1, 512, 512), dtype=float64>
      * properties: 'absolute_orbit', 'acquired', 'archived', 'area', ...
      * bandinfo: 'nir_sub_red_div_nir_add_red'
      * geocontext: 'geometry', 'key', 'resolution', 'tilesize', ...
    """
    return Workflow.get(workflow_id, client=client)


def use(workflow_id, client=None):
    """
    Use like ``import``: load the proxy object of a published `Workflow`.

    Shorthand for ``retrieve(workflow_id).object``.

    Parameters
    ----------
    workflow_id: str
        ID of the `Workflow` to retrieve
    client: `.workflows.client.Client`, optional
        Allows you to use a specific client instance with non-default
        auth and parameters

    Returns
    -------
    obj: Proxytype
        Proxy object of the `Workflow`.

    Example
    -------
    >>> from descarteslabs.workflows import Image, Function, use
    >>> def ndvi(img):
    ...     nir, red = img.unpack_bands("nir red")
    ...     return (nir - red) / (nir + red)
    >>> func = Function.from_callable(ndvi, Image) # create a function that can be called on an Image
    >>> workflow = func.publish("NDVI") # doctest: +SKIP
    >>> workflow.id # doctest: +SKIP
    '42cea96a864811f00f0bcdb8177ba80d6dc9c7492e13e794'
    >>> same_function = use('42cea96a864811f00f0bcdb8177ba80d6dc9c7492e13e794') # doctest: +SKIP
    >>> same_function # doctest: +SKIP
    <descarteslabs.workflows.types.function.function.Function[Image, {}, Image] object at 0x...>
    >>> img = Image.from_id("sentinel-2:L1C:2019-05-04_13SDV_99_S2B_v1")
    >>> same_function(img).compute(geoctx) # geoctx is an arbitrary geocontext for 'img' # doctest: +SKIP
    ImageResult:
    ...
    """
    return retrieve(workflow_id, client=client).object
