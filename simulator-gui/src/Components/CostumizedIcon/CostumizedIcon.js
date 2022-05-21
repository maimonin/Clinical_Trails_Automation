import React from 'react';
import PersonIcon from '@mui/icons-material/Person';
import { ImLab } from 'react-icons/im';
import stethoscope from '../../Assests/stethoscope.png'


export default function CostumizedIcon(props){
    const style = {color: props.sex==="male"?"cyan":props.sex==="female"?"pink":"grey"}

    const icons = {
        // "nurse" 
        "lab technician" : <ImLab style={style}/>
    }
    return(<PersonIcon style={style}/>)
}