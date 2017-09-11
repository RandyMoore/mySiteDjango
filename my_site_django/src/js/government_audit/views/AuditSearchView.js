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

function ResultsTable(props) {
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
         {props.searchResults.results && props.searchResults.results.map(function(result, index) {
           return <tr key={ index }>
             <td>{ props.searchResults.resultsOffset + index + 1 }</td>
             <td>
               <a href={ result.get('url') }>{ result.get('title') }</a>
             </td>
             <td> {result.get('date')} </td>
           </tr>;
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
