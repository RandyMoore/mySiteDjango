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
    searchResults: AuditSearchStore.getState(),

    onQueryChange: SearchActions.changeQuery,
    onParserChange: SearchActions.changeParser,
    onQuerySubmit: SearchActions.submitQuery,
    onPageChange: SearchActions.changePage,
  };
}

export default Container.createFunctional(AuditSearch, getStores, getState);
