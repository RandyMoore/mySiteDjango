import Dispatcher from './Dispatcher';
import SearchActionTypes from './SearchActionTypes';

const SearchActions = {
  changeQuery(event) {
    Dispatcher.dispatch({
      type: SearchActionTypes.CHANGE_QUERY,
      event,
    });
  },

  changeParser(event) {
    Dispatcher.dispatch({
      type: SearchActionTypes.CHANGE_PARSER,
      event,
    });
  },

  submitQuery(event) {
    Dispatcher.dispatch({
      type: SearchActionTypes.SUBMIT_QUERY,
      event,
    });
  },

  handleQueryResponse(response) {
    Dispatcher.dispatch({
      type: SearchActionTypes.LOAD_QUERY_RESPONSE,
      response,
    });
  },

  changePage(data) {
    Dispatcher.dispatch({
      type: SearchActionTypes.CHANGE_PAGE,
      data,
    });
  },
};

export default SearchActions;
