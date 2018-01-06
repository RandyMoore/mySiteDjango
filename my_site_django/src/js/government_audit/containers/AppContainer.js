import {
  Container
} from 'flux/utils';
import SearchActions from '../data/SearchActions';
import AuditSearchStore from '../data/SearchStore';
import AuditSearch from '../views/AuditSearchView'

function getStores() {
  return [
    AuditSearchStore,
  ];
}

function getState() {
  return {
    auditSearch: AuditSearchStore.getState(),

    onQueryChange: SearchActions.changeQuery,
    onYearSelectionChange: SearchActions.changeYearSelection,
    onParserChange: SearchActions.changeParser,
    onQuerySubmit: SearchActions.submitQuery,
    onDocumentPageChange: SearchActions.changeDocumentPage,
    onNamedEntityExplorationClick: SearchActions.changeEntityPage,
    onNamedEntityClick: SearchActions.searchNamedEntity,
    onEntityPageChange: SearchActions.changeEntityPage,
  };
}

export default Container.createFunctional(AuditSearch, getStores, getState);
