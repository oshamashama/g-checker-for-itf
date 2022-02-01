import React from 'react';
import ReactDOM from 'react-dom';
import './App.css';
import Data from './grade.json'
import { useTable } from "react-table";



class Table extends React.Component {
    render() {
        function zeroPadding(str) {
            return ('   ' + str).slice(-3);
        }


        let itemList = []
        for (const key in this.props.value) {
            let pushStr = zeroPadding(this.props.value[key]['now_certificated_credit_num'])
                + '/'
                + zeroPadding(this.props.value[key]['min_certificated_credit_num'])
            let passed = ""
            if (this.props.value[key]['now_certificated_credit_num'] >= this.props.value[key]['min_certificated_credit_num'])
                passed = "passed"
            else
                passed = "failed"
            itemList.push([key, pushStr, passed])
        }
        if (this.props.depth === 0) {
            return (
                <div className='con'>
                    {itemList.map(([key, st, passed]) => (
                        <div className={'bl_tate ' + passed} key={key}>
                            <p className='hight-center'>
                                {(key === "" ? "　　　　" : (key !== "専門基礎" ? "　" + key + "　" : key))
                                    + st}
                            </p>
                        </div>
                    ))}
                </div>
            )
        }

        return (
            <div className='con'>
                {itemList.map(([key, st, passed]) => (
                    <div className={'gre_yoko ' + passed} key={key}>
                        <div className={'bl_tate ' + passed} key={key}>
                            <p className='hight-center'>
                                {(key === "" ? "　　　　" : (key !== "専門基礎" ? "　" + key + "　" : key))
                                    + st}
                            </p>
                        </div>
                        <div className={'bl_tate ' + passed} key={key}>
                            <Table value={this.props.value[key]['leaf']} depth={this.props.depth - 1} />
                        </div>
                    </div>
                ))}
            </div>
        )
    }
}

function Main() {
    return (
        <div className="App">
            <header className="App-header">
                <Table value={Data} depth={4} />
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
