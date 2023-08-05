
# Type: data file




URI: [biolink:DataFile](https://w3id.org/biolink/vocab/DataFile)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[DataSetVersion]-%20source%20data%20file%200..1>[DataFile&#124;id(i):identifier_type;name(i):label_type;category(i):iri_type%20%2B],%20[DataFile]^-[SourceFile],%20[NamedThing]^-[DataFile])

## Parents

 *  is_a: [NamedThing](NamedThing.md) - a databased entity or concept/class

## Children

 * [SourceFile](SourceFile.md)

## Referenced by class

 *  **[DataSetVersion](DataSetVersion.md)** *[source data file](source_data_file.md)*  <sub>OPT</sub>  **[DataFile](DataFile.md)**

## Attributes


### Inherited from named thing:

 * [id](id.md)  <sub>REQ</sub>
    * Description: A unique identifier for a thing. Must be either a CURIE shorthand for a URI or a complete URI
    * range: [IdentifierType](types/IdentifierType.md)
    * inherited from: [NamedThing](NamedThing.md)
    * in subsets: (translator_minimal)
 * [name](name.md)  <sub>REQ</sub>
    * Description: A human-readable name for a thing
    * range: [LabelType](types/LabelType.md)
    * inherited from: [NamedThing](NamedThing.md)
    * in subsets: (translator_minimal)
 * [category](category.md)  <sub>1..*</sub>
    * Description: Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In a neo4j database this MAY correspond to the neo4j label tag
    * range: [IriType](types/IriType.md)
    * inherited from: [NamedThing](NamedThing.md)
    * in subsets: (translator_minimal)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Mappings:** | | EFO:0004095 |

