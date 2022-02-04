import React, { useState, Component } from 'react';
import ReactDOM from 'react-dom';
import './App.css';
import Data from './reqJson/coins20.json'
import { useTable } from "react-table";
import { readCsv } from './checkGraduate/readCsv.ts'
import { checkGraduate } from './checkGraduate/checkGrad.ts'
import Select from 'react-select'


class Table extends React.Component {
  render() {
    console.log("updateupdateupdateupdateupdateupdateupdateupdateupdateupdateupdateupdateupdate");
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
  let [GradeData, setGradeData] = useState();
  const [, rerender] = useState();

  const onFileInputChangeCSV = (e: React.ChangeEvent<HTMLInputElement>) => {
    // setJsonData(DefJsonData);
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = () => {
      // setGradeData(readCsv(reader.result));
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
    // console.log(f.value);
    var data = require('./reqJson/' + f.value);
    // console.log(data);
    setDefJsonData(data);
    setJsonData(DefJsonData);
    // const file = e.target.files[0];
    // const reader = new FileReader();
    // reader.onload = () => {
    //   setJsonData(JSON.parse(reader.result));
    // };
    // reader.readAsText(file);
  };

  const update = () => {
    console.log(GradeData);
  }
  const update2 = () => {
    console.log(JsonData)
  }
  const update3 = () => {
    checkGraduate(GradeData, JsonData, (res) => {
      setJsonData(res);
    });
  }
  const options = [
    { value: 'mast20.json', label: 'mast20' },
    { value: 'coins19.json', label: 'coins19' },
    { value: 'coins20.json', label: 'coins20' },
    { value: 'coins21.json', label: 'coins21' }
  ]

  return (
    <div className="App">
      <header className="App-Upload">
        <div>
          <a>
            target csv
          </a>
          <input type="file" onChange={onFileInputChangeCSV} />
          {/* </div> */}
          {/* <div>
          <a>
            requirements json
          </a>
          <input type="file" onChange={onFileInputChangeJSON} />
        </div> */}
          {/* <div> */}
          {/* <button onClick={update}>
            check csv
          </button>
          <button onClick={update2}>
            check json
          </button>
          <button onClick={update3}>
            update
          </button> */}
          {/* </div> */}
          {/* <div> */}
          <Select
            options={options}
            onChange={selectReq}
            defaultValue={{ value: 'coins20.json', label: 'coins20' }}
          />
          <button onClick={rerender}>
            rerender
          </button>
        </div>
      </header>
      <header className="App-header">
        <Table value={JsonData} depth={4} />
      </header>
    </div>
  );
}

function App() {
  return (
    <Main />
  );
}

export default App;
