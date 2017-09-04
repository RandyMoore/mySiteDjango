import React from 'react'
import ReactDOM from 'react-dom'
import ReactPaginate from 'react-paginate'
import axios from 'axios'

class Options extends React.Component {
  render() {
    return (
      <div>
        <a href="https://www.postgresql.org/docs/9.6/static/textsearch-controls.html"> Query Parser: </a>
        <select value={this.props.queryParser} onChange={this.props.onChange}>
          <option value="plain">plain</option>
          <option value="phrase">phrase</option>
          <option value="raw">tsquery raw</option>
        </select>
      </div>
    )
  }
}

class SearchInput extends React.Component {
  render() {
    return (
      <form onSubmit={this.props.onSubmit}>
        <label>
          Search Query <br/>
          <input type="text" value={this.props.query} onChange={this.props.onChange}/>
        </label>
        <input type="submit" value="Submit" />
      </form>
    )
  }
}

class ResultsList extends React.Component {
 render() {
   return (
   <ul>
      {this.props.results.map(function(result, index) {
       return <li key={ index }>
          <a href={ result.url }>{ result.title }</a>
        </li>;
      })}
    </ul>
   )}
}

class AuditSearch extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      query: '',
      queryParser:'plain',
      results: [],
      resultsOffset: 0,
      resultsLimit: 10,
      pageCount: 0
    };
  }

  handleQueryChange(event) {
    this.setState({query: event.target.value});
  }

  handleQueryTypeChange(event) {
    this.setState({queryParser: event.target.value})
  }

  handleQuerySubmit(event) {
    if (this.state.query === '') {
        return
    }

    axios.get('/audits/search/', {
      params: {
        query: this.state.query,
        parser: this.state.queryParser,
        limit: this.state.resultsLimit,
        offset: this.state.resultsOffset
      }
    }).then(res => {
      const results = res.data.results;
      const query = res.data.query;
      const size = res.data.size;
      this.setState({
        results: results,
        pageCount: Math.ceil(size / this.state.resultsLimit)
     });
    });

    if (event) { // Prevent default full page reload after hitting submit button for query
        event.preventDefault();
    }
  }

  handlePageClick(data) {
    let selected = data.selected;
    let offset = Math.ceil(selected * this.state.resultsLimit);

    this.setState({resultsOffset: offset}, () => {
        this.handleQuerySubmit(null);
    });
  }

  render() {
    const query = this.state.query;
    const queryParser = this.state.queryParser;
    const results = this.state.results;

    return (
      <div>
        <SearchInput
          query={query}
          onChange={event => this.handleQueryChange(event)}
          onSubmit={event => this.handleQuerySubmit(event)} />
        <Options
          queryParser={queryParser}
          onChange={event => this.handleQueryTypeChange(event)} />
        <ResultsList
          results= {results} />
        { this.state.pageCount > 1 &&
          <ReactPaginate
            previousLabel={"previous"}
            nextLabel={"next"}
            breakLabel={<a href="">...</a>} // TODO update href to retain state
            breakClassName={"break-me"}
            pageCount={this.state.pageCount}
            marginPagesDisplayed={2}
            pageRangeDisplayed={5}
            onPageChange={this.handlePageClick.bind(this)}
            containerClassName={"pagination"}
            subContainerClassName={"pages pagination"}
            activeClassName={"active"} /> }
      </div>
    )
  }
}

ReactDOM.render(
    React.createElement(AuditSearch, window.props),
    window.react_mount,
)
