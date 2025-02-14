```mermaid

block-beta
columns 1
  block:ID
    A["Presentation Layer
    User
    API
    Place"]
    space
    B["Business Logic Layer
    Business Façade
    Domain"]
    space
    C["Persistence Layer
    Database
    Repository"]
  end
  space
  A --> B
  B --> C