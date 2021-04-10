import React, { Component } from 'react';

const table =[];
for (let i=0; i<9; i++){
    table.push(
    <tr>
<td contentEditable='true' min="1" max="9"></td>
<td contentEditable='true' min="1" max="9"></td>
<td contentEditable='true' min="1" max="9"></td>
<td contentEditable='true' min="1" max="9"></td>
<td contentEditable='true' min="1" max="9"></td>
<td contentEditable='true' min="1" max="9"></td>
<td contentEditable='true' min="1" max="9"></td>
<td contentEditable='true' min="1" max="9"></td>
<td contentEditable='true' min="1" max="9"></td>
</tr>)}

class Grid extends Component { 
    render() {
        return (
            <div className="grid">
             <table className="sudokuTable">
             {table}
      </table>   
            </div>
        )
    }
}

export default Grid;