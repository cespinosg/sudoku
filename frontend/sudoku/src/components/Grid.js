import React, { Component } from "react";

const array = Array(81).fill(0); // create array to store all values of sudoku

//subdivide array into groups of 9 (length of row)
const perRow = 9; // items per row
const dividedArray = array.reduce((resultArray, item, index) => {
  const chunkIndex = Math.floor(index / perRow);

  if (!resultArray[chunkIndex]) {
    resultArray[chunkIndex] = []; // start a new chunk
  }

  resultArray[chunkIndex].push(item);

  return resultArray;
}, []);

class Grid extends Component {
  constructor(props) {
    super(props);
    this.state = { dividedArray };
  }

  handleChange(e) {
    console.log("handle change", e);
    // this.setState({ dividedArray: e.target.value }); // need to figure out how to know what value to update
  }
  handleClick(k) {
    console.log("click!"); // TODO send form to backend for resolution
    const arraySdm = this.state.dividedArray.join();
    console.log(arraySdm);
  }
  render() {
    console.log(this.state);
    return (
      <div className="grid">
        Please, input the values in the table below
        <table>
          <tbody>
            {this.state.dividedArray.map((numList, i) => (
              <tr key={i}>
                {numList.map((num, j) => (
                  <td key={j}>
                    <input
                      type="number"
                      value={num}
                      contentEditable="true"
                      onChange={(e) => {
                        this.handleChange(e);
                      }}
                    />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        <button onClick={(k) => this.handleClick(k)} autoFocus>
          Solve Sudoku!
        </button>
      </div>
    );
  }
}

export default Grid;
