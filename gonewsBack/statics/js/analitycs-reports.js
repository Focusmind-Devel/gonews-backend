gapi.analytics.ready(function() {

    /**
     * Authorize the user immediately if the user has already granted access.
     * If no access has been created, render an authorize button inside the
     * element with the ID "embed-api-auth-container".
     */
    gapi.analytics.auth.authorize({
      container: 'embed-api-auth-container',
      clientid: '639021655317-ubm51ufeolsogsn9fo8str2b1s6iq8e5.apps.googleusercontent.com'
    });
  
  
    /**
     * Create a new ViewSelector instance to be rendered inside of an
     * element with the id "view-selector-container".
     */
  
    /**
     * Store a set of common DataChart config options since they're shared by
     * both of the charts we're about to make.
     */
    var commonConfig = {
      query: {
        metrics: 'ga:sessions',
        dimensions: 'ga:hour',
        
        'start-date':'today',
        'end-date':'today',
      },
      chart: {
        type: 'LINE',
        options: {
          width: '600px',
          crosshair:{color:'#E71D36',focused: { color: '#3bc', opacity: 0.8 } },
          chartArea:{width:'100%'},
          colors:['#E71D36']
        }
      }
    };
  
  
    
  
  
  
    /**
     * Create a new ViewSelector2 instance to be rendered inside of an
     * element with the id "view-selector-container".
     */
    var viewSelector = new gapi.analytics.ext.ViewSelector2({
      container: 'view-selector-container',
    }).execute();
  
  
    /**
     * Create a new DateRangeSelector instance to be rendered inside of an
     * element with the id "date-range-selector-1-container", set its date range
     * and then render it to the page.
     */
    
  
  
  
    /**
     * Create a new DataChart instance with the given query parameters
     * and Google chart options. It will be rendered inside an element
     * with the id "data-chart-1-container".
     */
    var dataChart1 = new gapi.analytics.googleCharts.DataChart(commonConfig)
        .set({chart: {container: 'data-chart-1-container'}});
  
  
  
  
    /**
     * Register a handler to run whenever the user changes the view.
     * The handler will update both dataCharts as well as updating the title
     * of the dashboard.
     */
    viewSelector.on('viewChange', function(data) {
      dataChart1.set({query: {ids: data.ids}}).execute();
  
      var title = document.getElementById('view-name');
      title.textContent = data.property.name + ' (' + data.view.name + ')';
    });
  

    document.getElementById('filter-today').addEventListener('click',(e)=>{
        toggleClass(e)
        dataChart1.set({query: {
            dimensions: 'ga:hour',
            'start-date': 'today',
            'end-date': 'today'
          }}).execute();
    })

    document.getElementById('filter-week').addEventListener('click',(e)=>{
        toggleClass(e)
        dataChart1.set({query: {
            dimensions: 'ga:date',
            'start-date': '7daysAgo',
            'end-date': 'today'
          }}).execute();
    })

    document.getElementById('filter-month').addEventListener('click',(e)=>{
        toggleClass(e)
        dataChart1.set({query: {
            dimensions: 'ga:date',
            'start-date': '30daysAgo',
            'end-date': 'today'
          }}).execute();
    })

    function toggleClass(e){
        document.querySelector('.activate').classList.remove('activate');
        e.target.classList.add('activate');
    }


    // nuevo


    // Replace with your view ID.
  var VIEW_ID = 'ga:226631686';

  // Query the API and print the results to the page.
 
    gapi.client.request({
      path: '/v4/reports:batchGet',
      root: 'https://analyticsreporting.googleapis.com/',
      method: 'POST',
      body: {
        reportRequests: [
          {
            viewId: VIEW_ID,
            dateRanges: [
              {
                startDate: '7daysAgo',
                endDate: 'today'
              }
            ],
            metrics: [
              {
                expression: 'ga:sessions'
              }
            ],
            dimensions: [
                {
                  name: 'ga:pagePath'
                }
              ]
          },
          {
            viewId: VIEW_ID,
            dateRanges: [
              {
                startDate: '7daysAgo',
                endDate: 'today'
              }
            ],
            metrics: [
              {
                expression: 'ga:sessions'
              }
            ],
            dimensions: [
                {
                  name: 'ga:pagePath'
                }
              ]
          }
        ]
      }
    }).then(displayResults, console.error.bind(console));

  function displayResults(response) {
    report = response.result.reports[0]
    selector = document.getElementById('filter-page');
    report.data.rows.forEach(element => {
        selector.options[selector.options.length] = new Option(element.dimensions[0],element.dimensions[0]);
    });
  }

  document.getElementById('filter-page').addEventListener('change',(e)=>{
      dataChart1.set({query: {
        filter:'ga:pagePath%3D%3D'+e.target.value
      }}).execute();
  })

  
  
  
  });