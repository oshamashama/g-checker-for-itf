import React, { useState } from 'react';
import './App.css';
import Data from './reqJson/coins20.json'
import { readCsv } from './checkGraduate/readCsv.ts'
import { checkGraduate } from './checkGraduate/checkGrad.ts'
import Select from 'react-select'
import 'bootstrap/dist/css/bootstrap.min.css';
import Button from 'react-bootstrap/Button';

class Table extends React.Component {
  render() {
    let itemList = []
    for (const key in this.props.value) {
      let pushStr = ' ' + (this.props.value[key]['now_certificated_credit_num'] === undefined ? 0 : this.props.value[key]['now_certificated_credit_num'])
        + '('
        + (this.props.value[key]['feature_certificated_credit_num'] === undefined ? 0 : this.props.value[key]['feature_certificated_credit_num'])
        + ')/'
        + (this.props.value[key]['min_certificated_credit_num'] === undefined ? 0 : this.props.value[key]['min_certificated_credit_num'])
      let passed = ""
      if (this.props.value[key]['now_certificated_credit_num'] >= this.props.value[key]['min_certificated_credit_num'])
        passed = "passed"
      else if (this.props.value[key]['now_certificated_credit_num'] + this.props.value[key]['feature_certificated_credit_num'] >= this.props.value[key]['min_certificated_credit_num'])
        passed = "expect"
      else
        passed = "failed"
      itemList.push([key, pushStr, passed])
    }
    if (this.props.depth === 0) {
      return (
        <div className='con'>
          {itemList.map(([key, st, passed]) => (
            <div className={'bl_tate ' + passed} key={key + st}>
              <p className='hight-center last-leaf'>
                {(key === "" ? "" : key) + st}
              </p>
            </div>
          ))}
        </div>
      )
    }

    return (
      <div className='con'>
        {itemList.map(([key, st, passed]) => (
          <div className={'gre_yoko ' + passed} key={key + st}>
            <div className={'bl_tate ' + passed} key={key + st + 'top'}>
              <p className='hight-center'>
                {(key === "" ? "" : key)}
              </p>
              <p className='hight-center'>
                {st}
              </p>
            </div>
            <div className={'bl_tate2 ' + passed} key={key + st}>
              <Table value={this.props.value[key]['leaf']} depth={this.props.depth - 1} />
            </div>
          </div>
        ))}
      </div>
    )
  }
}

function Main() {
  let [JsonData, setJsonData] = useState(Data);
  let [DefJsonData, setDefJsonData] = useState(Data);
  // let [GradeData, setGradeData] = useState();
  const [, rerender] = useState();

  const onFileInputChangeCSV = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = () => {
      setJsonData(DefJsonData);
      checkGraduate(readCsv(reader.result), JsonData, (res) => {
        setJsonData(res);
      });
    };
    reader.readAsText(file);
  };

  const onFileInputChangeJSON = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = () => {
      setJsonData(JSON.parse(reader.result));
    };
    reader.readAsText(file);
  };
  const selectReq = (f) => {
    var data = require('./reqJson/' + f.value);
    setDefJsonData(data);
    setJsonData(DefJsonData);
  };

  const options = [
    { value: 'mast20.json', label: 'mast20' },
    { value: 'coins19.json', label: 'coins19' },
    { value: 'coins20.json', label: 'coins20' },
    { value: 'coins21.json', label: 'coins21' }
  ]

  return (
    <div className="App">
      <div className="App-Upload">
        <div>
          <input type="file" onChange={onFileInputChangeCSV} />
          <Select
            options={options}
            onChange={selectReq}
            defaultValue={{ value: 'coins20.json', label: 'coins20' }}
          />
          <Button onClick={rerender}>
            rerender
          </Button>
        </div>
      </div>
      <div className="App-main">
        <Table value={JsonData} depth={4} />
      </div>
    </div>
  );
}

function App() {
  return (
    <Main />
  );
}

export default App;
