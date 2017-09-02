import React from 'react'
import ReactDOM from 'react-dom'
import axios from 'axios'

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

class SearchResult extends React.Component {
  render() {
    <li>

    </li>
  }
}

class AuditSearch extends React.Component {
  constructor(props) {
    super(props);
    this.state = {query: '', results: []};
  }

  handleChange(event) {
    this.setState({query: event.target.value});
  }

  handleSubmit(event) {
    axios.get(`/audits/search/?query=${this.state.query}`)
      .then(res => {
        const results = res.data.results;
        this.setState({ query: '', results: results });
      });
    event.preventDefault();
  }

  render() {
    const query = this.state.query;

    return (
      <div>
        <SearchInput
          query={query}
          onChange={event => this.handleChange(event)}
          onSubmit={event => this.handleSubmit(event)}
        />
        <ul>
          {this.state.results.map(function(result, index) {
           return <li key={ index }>
              <a href={ result.url }>{ result.title }</a>
            </li>;
          })}
        </ul>
      </div>
    )
  }
}

ReactDOM.render(
    React.createElement(AuditSearch, window.props),
    window.react_mount,
)
