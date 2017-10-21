import React from 'react';
import ReactPaginate from 'react-paginate';
import Immutable from 'immutable';

function QueryParserOption(props) {
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
        <input type="text" value={props.auditSearch.query} onChange={props.onQueryChange}/>
      </label>
      <input type="submit" value="Submit" />
    </form>
  );
}

const YearSelections = Immutable.List(
  [
    'before2014',
    '2014',
    '2015',
    '2016',
    '2017'
  ]
);

function YearSelection(props) {
  return (
      <fieldset className="year-selection right">
        { YearSelections.map( yearSelection => {
            return (
              <span key={yearSelection}>
                <input
                  type="checkbox"
                  id={yearSelection}
                  name="yearSelection"
                  value={yearSelection}
                  onChange={props.onYearSelectionChange}
                  checked={props.auditSearch.years.includes(yearSelection)} />
                <label className="year-selection-label" htmlFor={yearSelection}>{yearSelection}</label>
              </span>
            );
          })
        }
      </fieldset>
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
  const results = props.auditSearch.results.toJS();

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
                key={ counter }
                rowNumber={ counter + 1 }
                result={ results[key] }
                resultsOffset={ props.auditSearch.resultsOffset } />
            );

            counter += 1;
            return jsx;
          })}
       </tbody>
    </table>
  );
}

function NamedEntityHistoryStack(props) {

}

function NamedEntityResults(props) {
  const namedEntities = props.auditSearch.namedEntityResults.toJS();

  return (
    <table>
      <thead>
        <tr>
          <th width="80%"> Name </th>
          <th> #Docs </th>
        </tr>
      </thead>
      <tbody>
        {namedEntities.map(ne => {
          return (
            <tr key={ ne.name } onClick={props.onNamedEntityClick}>
              <td> { ne.name } </td>
              <td> { ne.numDocs } </td>
            </tr>
          );
        })}
     </tbody>
    </table>
  );
}

function NamedEntityExploration(props) {
  return (
    <div>
      <button id="ne-exploration-heading" onClick={props.onNamedEntityClick}>Named Entity Exploration</button>
      <NamedEntityResults {...props} />
    </div>
  );
}

function AuditSearchComponent(props) {
  const pageCount = Math.ceil(props.auditSearch.resultsSize / props.auditSearch.resultsLimit)
  const currentPage = Math.floor(props.auditSearch.resultsOffset / props.auditSearch.resultsLimit)
  return (
    <div>
      <SearchInput {...props} />
      <QueryParserOption {...props} />
      <br/>
      <YearSelection {...props} />
      <br/>
      <NamedEntityExploration {...props} />
      <h3 className="heading">Results:</h3>
      <ResultsTable {...props} />
      { pageCount > 1 &&
        <ReactPaginate {...props}
          forcePage={currentPage}
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

export default AuditSearchComponent;
