#ifndef AMPL_ENTITYMAP_H
#define AMPL_ENTITYMAP_H

#include <map>
#include <iterator>

#include "ampl/entity.h"

namespace ampl {
/**
 * Represents a synchronised list of %AMPL entities. It can be obtained using
 * the functions AMPL::getVariables(), AMPL::getConstraints(), AMPL::getSets(),
 * AMPL::getObjectives(), AMPL::getParameters(). <p> The collection cannot be
 * modified by the user (entities cannot be added nor deleted) and is linked to
 * an AMPL object. When the corresponding %AMPL entities are modified (through
 * AMPL::eval() or any other operation which influences the number of entities),
 * the collection is automatically invalidated. It is updated lazily at the next
 * access. <p> If the corresponding AMPL object is not running anymore, or it is
 * null, an exception is thrown on all operations.
 */
template <class EntityClass>
class EntityMap {
  friend class AMPL;

 public:
  class iterator {
    public:
      iterator() : _it() {}
      explicit iterator(typename std::map<std::string, EntityClass>::iterator it) : _it(it) {}
      iterator& operator++() { ++_it; return *this; }
      iterator operator++(int) { iterator tmp = *this; ++_it; return tmp; }
      bool operator==(const iterator& other) const { return _it == other._it; }
      bool operator!=(const iterator& other) const { return _it != other._it; }
      EntityClass& operator*() const { return _it->second; }
      EntityClass* operator->() const { return &(_it->second); }

    private:
      typename std::map<std::string, EntityClass>::iterator _it;
    };

  /**
  Entity access
  Returns the entity identified by the specified name.
  \param name Name of the entity to be found
  \return The entity with the corresponding name
  \throws An std::out_of_range exception if the specified parameter does not
  exist
  */
  EntityClass& operator[](fmt::CStringRef name) const {
    std::string str(name.c_str());
    return *find(str);
  }

  /**
   * Get the number of items in the collection
   */
  std::size_t size() const {
    return entity_map_.size();
  }

  /**
  Return an iterator to the beginning of this collection. Use together
  with end() to iterate through the contents of this list.
  \rst
  An example, printing the names of all the variables defined in the AMPL object
  named ``ampl``::

    for (ampl::Variable v: ampl.getVariables())
      std::cout << v.name() << "\n";
  \endrst
  */
  iterator begin() const {
    return iterator(entity_map_.begin());
  }

  /**
  Return iterator to the end of this collection
  */
  iterator end() const {
    return iterator(entity_map_.end());
  }

  /**

  Searches the container for an entity with the specified
   name and returns an iterator to it if found, otherwise
    it returns an iterator to end().

  \rst

  An example which checks if the variable ``x`` is defined in the
  AMPL object called ``ampl``::

    ampl::EntityMap<Variable> vars = ampl.getVariables();
    ampl::EntityMap<Variable>::iterator it = vars.find("x");
    if(it == vars.end())
      std::cout << "Variable x does not exist\n");

  \endrst

  \param name The name of the entity to be found
  \return An iterator to the entity, if an Entity with specified key is
  found, or end() otherwise.

  */
  iterator find(std::string name) const {
    return iterator(entity_map_.find(name));
  }

 protected:
  ::AMPL *ampl_;
  AMPL_ENTITYTYPE type_;
  mutable std::map<std::string, EntityClass> entity_map_;

 private:
  explicit EntityMap(::AMPL *ampl, AMPL_ENTITYTYPE type) : ampl_(ampl), type_(type) { 
    char **names;
    size_t size;
    switch (type_) {
      case AMPL_VARIABLE:
        AMPL_CALL_CPP(AMPL_GetVariables(ampl_, &size, &names));
        for (size_t i=0; i<size; i++) {
          EntityClass entity(ampl_, names[i]);
          std::string str(names[i]);
          entity_map_.insert(std::pair<std::string, EntityClass>(str, entity));
          AMPL_StringFree(&names[i]);
        }
        free(names);
        break;
      case AMPL_CONSTRAINT:
        AMPL_CALL_CPP(AMPL_GetConstraints(ampl_, &size, &names));
        for (size_t i=0; i<size; i++) {
          EntityClass entity(ampl_, names[i]);
          std::string str(names[i]);
          entity_map_.insert(std::pair<std::string, EntityClass>(str, entity));
          AMPL_StringFree(&names[i]);
        }
        free(names);
        break;
      case AMPL_OBJECTIVE:
        AMPL_CALL_CPP(AMPL_GetObjectives(ampl_, &size, &names));
        for (size_t i=0; i<size; i++) {
          EntityClass entity(ampl_, names[i]);
          std::string str(names[i]);
          entity_map_.insert(std::pair<std::string, EntityClass>(str, entity));
          AMPL_StringFree(&names[i]);
        }
        free(names);
        break;
      case AMPL_PARAMETER:
        AMPL_CALL_CPP(AMPL_GetParameters(ampl_, &size, &names));
        for (size_t i=0; i<size; i++) {
          EntityClass entity(ampl_, names[i]);
          std::string str(names[i]);
          entity_map_.insert(std::pair<std::string, EntityClass>(str, entity));
          AMPL_StringFree(&names[i]);
        }
        free(names);
        break;
      case AMPL_SET:
        AMPL_CALL_CPP(AMPL_GetSets(ampl_, &size, &names));
        for (size_t i=0; i<size; i++) {
          EntityClass entity(ampl_, names[i]);
          std::string str(names[i]);
          entity_map_.insert(std::pair<std::string, EntityClass>(str, entity));
          AMPL_StringFree(&names[i]);
        }
        free(names);
        break;
      case AMPL_PROBLEM:
        AMPL_CALL_CPP(AMPL_GetProblems(ampl_, &size, &names));
        for (size_t i=0; i<size; i++) {
          EntityClass entity(ampl_, names[i]);
          std::string str(names[i]);
          entity_map_.insert(std::pair<std::string, EntityClass>(str, entity));
          AMPL_StringFree(&names[i]);
        }
        free(names);
        break;
      default:
        break;
    }
  }

};
}  // namespace ampl
#endif  // AMPL_ENTITYMAP_H
