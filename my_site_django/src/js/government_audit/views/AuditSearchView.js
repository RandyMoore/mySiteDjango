import React from 'react';
import ReactPaginate from 'react-paginate';

function Options(props) {
  return (
    <div>
      <a href="https://www.postgresql.org/docs/9.6/static/textsearch-controls.html"> Query Parser: </a>
      <select value={props.queryParser} onChange={props.onParserChange}>
        <option value="plain">plain</option>
        <option value="phrase">phrase</option>
        <option value="raw">tsquery raw</option>
      </select>
    </div>
  );
}

function SearchInput(props) {
  return (
    <form onSubmit={props.onQuerySubmit}>
      <label>
        Search Query <br/>
        <input type="text" value={props.searchResults.query} onChange={props.onQueryChange}/>
      </label>
      <input type="submit" value="Submit" />
    </form>
  );
}

function ResultRow(props) {
  function getCSSForTitle(urlActive) {
    switch(props.result.isActive) {
      case true:
        return {color: '#0000FF', fontStyle: 'normal'};
      case false:
        return {color: '#FF0000', fontStyle: 'normal', textDecoration: 'line-through'};
      default: // Not known if url is active yet, initial state
        return {color: '#708090', fontStyle: 'italic'};
    }
  };

  const resultStyle = getCSSForTitle(props.result.isActive);

  return (
    <tr>
      <td>{ props.resultsOffset + props.rowNumber}</td>
      <td>
        <a href={ props.result.url } style={ resultStyle }> { props.result.title }</a>
      </td>
      <td> { props.result.date } </td>
    </tr>
  );
}

function ResultsTable(props) {
  const results = props.searchResults.results.toJS();

  let counter = 0;
  return (
    <table className="results-table">
      <thead>
        <tr>
          <th/>
          <th width="80%">Title</th>
          <th>Publication Date</th>
         </tr>
        </thead>
        <tbody>
          {results && Object.keys(results).map(key => {
            const jsx = (
              <ResultRow
                key={counter}
                rowNumber={counter + 1}
                result={ results[key] }
                resultsOffset={ props.searchResults.resultsOffset } />
            );

            counter += 1;
            return jsx;
          })}
       </tbody>
    </table>
  );
}

function AuditSearch(props) {
  const pageCount = Math.ceil(props.searchResults.resultsSize / props.searchResults.resultsLimit)
  return (
    <div>
      <SearchInput {...props} />
      <Options {...props} />
      <ResultsTable {...props} />
      { pageCount > 1 &&
        <ReactPaginate {...props}
          previousLabel={"previous"}
          nextLabel={"next"}
          breakLabel={<a>...</a>}
          breakClassName={"break-me"}
          pageCount={pageCount}
          marginPagesDisplayed={2}
          pageRangeDisplayed={5}
          onPageChange={props.onPageChange}
          containerClassName={"pagination"}
          subContainerClassName={"pages pagination"}
          activeClassName={"active"}
        />
      }
    </div>
  );
}

export default AuditSearch;
