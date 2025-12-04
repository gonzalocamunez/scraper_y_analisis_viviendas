# ====== Selectors (actualizados) y modelo de datos ======
SELECTORS: Dict[str, str] = {
    # Dato 'precio'
    "precio": (
        "#main > div > main > section.detail-info.ide-box-detail-first-picture."
        "ide-box-detail--reset.overlay-box > section > div.info-data > span > span"
    ),
    # Dato 'piso__ext_int_ascensor' (m2, habitaciones, piso/exterior/ascensor). Seguimos usando el contenedor de spans y extraemos el triple en orden
    "info_features_spans": ".info-features > span",
    # Listado de datos 'detalles' (contenedor completo: queremos el texto de todos los hijos)
    "detalles": (
        "#main > div > main > section.detail-info.ide-box-detail-first-picture."
        "ide-box-detail--reset.overlay-box > section > div.info-features"
    ),
    # Listado de datos 'caracteristicas_basicas' (usar li para obtener cada ítem)
    "caracteristicas_basicas": (
        "#details > div.details-property > div.details-property-feature-one > div > ul li"
    ),
    # Listado de datos 'edificio' (usar li para obtener cada ítem)
    "edificio": (
        "#details > div.details-property > div.details-property-feature-one > div:nth-child(4) > ul li"
    ),
    # Listado de datos 'equipamiento' (usar li para obtener cada ítem)
    "equipamiento": (
        "#details > div.details-property > div.details-property-feature-two > div:nth-child(2) > ul li"
    ),
    # Listado de datos 'certificado_energetico' (usar li para obtener cada ítem)
    "certificado_energetico": (
        "#details > div.details-property > div.details-property-feature-two > div:nth-child(4) > ul li"
    ),
}


@dataclass
class Anuncio:
    precio: str
    m2: str
    habitaciones: str
    piso__ext_int_ascensor: str
    detalles: List[str]
    caracteristicas_basicas: List[str]
    edificio: List[str]
    equipamiento: List[str]
    certificado_energetico: List[str]