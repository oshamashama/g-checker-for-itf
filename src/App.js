import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import './App.css';
import Data from './grade.json'
import { useTable } from "react-table";



class Table extends React.Component {
    render() {
        let itemList = []
        for (const key in this.props.value) {
            let pushStr = ' ' + (this.props.value[key]['now_certificated_credit_num'])
                + '('
                + this.props.value[key]['feature_certificated_credit_num']
                + ')/'
                + (this.props.value[key]['min_certificated_credit_num'])
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

    const onFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files[0];
        const reader = new FileReader();
        reader.onload = () => {
            setJsonData(JSON.parse(reader.result));
        };
        reader.readAsText(file);
    };

    return (
        <div className="App">
            <header className="App-Upload">
                <div>
                    <input type="file" onChange={onFileInputChange} />
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
