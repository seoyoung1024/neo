document.addEventListener("DOMContentLoaded", function() {
    const ageGroupYearRanges = {
      17: {start: "2015-01-01", end: "2025-12-31"},
      22: {start: "2015-01-01", end: "2025-12-31"},
      27: {start: "2010-01-01", end: "2025-12-31"},
      32: {start: "2005-01-01", end: "2025-12-31"},
      37: {start: "2000-01-01", end: "2025-12-31"},
    };
  
    // 세대 라벨 매핑
    const ageGroupLabels = {
      17: "Z세대 후반 (17~21세)",
      22: "Z세대 중심 (22~26세)",
      27: "밀레니얼 후반 (27~31세)",
      32: "밀레니얼 중반 (32~36세)",
      37: "밀레니얼 초반 (37~41세)"
    };
  
    let genreChart = null;
    document.getElementById('searchForm').onsubmit = async function(e) {
      e.preventDefault();
      this.style.display = 'none';
      const ageGroup = this.ageGroup.value;
      const range = ageGroupYearRanges[ageGroup];
      const startDt = range.start;
      const endDt = range.end;
      // 서버 라우터로 GET 요청 (쿼리스트링)
      const params = new URLSearchParams({ ageGroup, startDt, endDt });
      const res = await fetch(`/genre-change?${params.toString()}`);
      const data = await res.json();
      console.log('data:', data);
      console.log('labels:', data.labels);
      console.log('datasets:', data.datasets);
      console.log('Chart:', typeof Chart);
      console.log('ChartDataLabels:', typeof ChartDataLabels);

      // 선택한 세대 라벨 동적 생성
      const ageLabel = ageGroupLabels[ageGroup] || "";

      // Chart.js 차트 그리기 (막대 중앙정렬용 dummy dataset 적용)
      let chartDatasets = data.datasets;
      if (data.datasets.length === 1) {
        // 단일 dataset일 때만 dummy dataset 추가
        const dummyData = new Array(data.labels.length).fill(0);
        chartDatasets = [
          {
            label: 'dummy',
            data: dummyData,
            backgroundColor: 'rgba(0,0,0,0)',
            borderWidth: 0,
            hoverBackgroundColor: 'rgba(0,0,0,0)',
            hoverBorderColor: 'rgba(0,0,0,0)'
          },
          data.datasets[0]
        ];
      }
      if (data.labels && chartDatasets) {
        const ctx = document.getElementById('genreChart').getContext('2d');
        if (genreChart) genreChart.destroy();
        genreChart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: data.labels,
            datasets: chartDatasets
          },
          options: {
            plugins: {
              tooltip: {
                enabled: true,
                backgroundColor: '#fff',
                titleColor: '#222',
                bodyColor: '#555',
              },
              legend: {
                position: 'top',
                labels: { font: { size: 14, family: 'Montserrat' }, color: '#333' }
              },
              title: {
                display: true,
                text: `${ageLabel}의 독서 성향 분석 결과`,
                font: { size: 24, family: 'Montserrat', weight: 'bold' },
                color: '#222'
              },
              datalabels: {
                color: 'white',
                display: function(context) {
                  return context.dataset.data[context.dataIndex] > 15;
                },
                font: { weight: 'bold' },
                formatter: function(value, context) {
                  return Math.round(value) + '권';
                }
              }
            },
            elements: {
              bar: {
                borderSkipped: false
              }
            },
            animation: {
              duration: 450,
              easing: 'linear',
              delay: function(ctx) {
                if (ctx.type === 'data' && ctx.mode === 'default' && ctx.dataIndex !== undefined) {
                  return ctx.dataIndex * 150; 
                }
                return 0;
              }
            },
            layout: {
              padding: {
                top: 24,
                right: 16,
                bottom: 0,
                left: 8
              }
            },
            aspectRatio: 5 / 3,
            scales: {
              x: {
                ticks: { font: { size: 12 }, color: '#222' },
                grid: { color: '#eee' },
                categoryPercentage: 0.4,
                barPercentage: 0.7,
                stacked: true
              },
              y: {
                beginAtZero: true,
                ticks: { font: { size: 12 }, color: '#222' },
                grid: { color: '#eee' },
                stacked: true
              }
            }
          },
          plugins: [ChartDataLabels]
        });
        document.getElementById('graph-container').style.display = 'block';

        // 인기 도서 표 출력
        if (data.topBooks && data.topBooks.length > 0) {
          let html = '<table class="top-books-table"><thead><tr><th>년도</th><th>장르</th><th>인기 도서</th><th>대출수</th></tr></thead><tbody>';
          data.topBooks.forEach(book => {
            html += `<tr>
              <td>${book.year}</td>
              <td>${book.classNm}</td>
              <td>${book.title}</td>
              <td>${book.loanCount}</td>
            </tr>`;
          });
          html += '</tbody></table>';
          document.getElementById('top-books').innerHTML = html;
        } else {
          document.getElementById('top-books').innerHTML = '';
        }
      } else {
        document.getElementById('graph-container').style.display = 'none';
      }
    }
});
