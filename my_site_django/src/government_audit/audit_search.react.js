import React from 'react'
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

class ResultsTable extends React.Component {
 render() {
   const resultsOffset = this.props.resultsOffset;

   return (
     <table className="results-table">
       <tr>
        <th/>
        <th width="80%">Title</th>
        <th>Publication Date</th>
       </tr>
        {this.props.results.map(function(result, index) {
          return <tr key={ index }>
            <td>{ resultsOffset + index + 1 }</td>
            <td>
              <a href={ result.url }>{ result.title }</a>
            </td>
            <td> {result.date} </td>
          </tr>;
        })}
    </table>
   )}
}

export default class AuditSearch extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      query: '',
      queryParser: 'plain',
      results: [],
      resultsOffset: 0,
      resultsLimit: 10,
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

    // Mark the fetch as attempted (regardless of result)
    this.state.fetchedQuery = this.state.query;

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
        <ResultsTable
          results={results}
          resultsOffset={this.state.resultsOffset} />
        { this.state.pageCount > 1 &&
          <ReactPaginate
            previousLabel={"previous"}
            nextLabel={"next"}
            breakLabel={<a>...</a>}
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
