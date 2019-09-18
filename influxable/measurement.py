class MeasurementMeta(type):
    def __init__(cls, name, *args, **kwargs):
        super(MeasurementMeta, cls).__init__(name, *args, **kwargs)
        attribute_names = cls._get_attribute_names()
        cls._extend_fields(attribute_names)

        get_query = cls._factory_get_query()
        setattr(cls, 'get_query', get_query)

