import React from 'react';
import ReactDOM from 'react-dom';
import './App.css';
import Data from './sample-coins20.json'
import { useTable } from "react-table";


class Img extends React.Component {
    // function Img() {
    render() {
        let sampleText = "ai";
        console.log("----\n")
        for (const k1 in Data) {
            console.log(k1 + ' : ' + Data[k1]['leaf']);
            for (const k2 in Data[k1]['leaf']) {
                console.log(k1 + '/' + k2 + ' : ' + Data[k1]['leaf'][k2]);
                for (const k3 in Data[k1]['leaf'][k2]['leaf']) {
                    console.log(k1 + '/' + k2 + '/' + k3 + ' : ' + Data[k1]['leaf'][k2]['leaf'][k3]);
                }
            }
        }
        return (
            <div className="Img" >
                <p>
                    {Data.情報科学類.leaf.基礎.leaf.共通.leaf.必修.leaf.総合科目.max_certificated_credit_num}
                </p>
                <p>
                    {sampleText}
                </p>
            </div>
        );
    }
}

class Table extends React.Component {
    render() {

        let itemList = []
        for (const key in this.props.value) {
            let pushStr = this.props.value[key]['now_certificated_credit_num']
                + ' / '
                + this.props.value[key]['min_certificated_credit_num']
            itemList.push([key, pushStr])
        }
        if (this.props.depth === 0) {
            return (
                <div className='con'>
                    {itemList.map(([key, st]) => (
                        <div className='bl_tate' key={key}>
                            <p className='hight-center'>
                                {key === "" ? "-" : '/' + key}
                            </p>
                            {/* + '  -  ' + st} */}
                        </div>
                    ))}
                </div>
            )
        }

        return (
            <div className='con'>
                {itemList.map(([key, st]) => (
                    <div className='gre_yoko' key={key}>
                        <div className='bl_tate' key={key}>
                            <p className='hight-center'>
                                {key === "" ? "-" : '/' + key}
                            </p>
                            {/* + '  -  ' + st} */}
                        </div>
                        <div className='bl_tate' key={key}>
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
