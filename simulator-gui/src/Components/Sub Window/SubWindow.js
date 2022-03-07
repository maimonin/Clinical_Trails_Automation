import React, {useState} from 'react';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import PersonIcon from '@mui/icons-material/Person';
import Box from '@mui/material/Box';

import MoreVertIcon from '@mui/icons-material/MoreVert';
import Question from '../Question/Question';



export default function SubWindow() {
    const [state,setState] = useState(1);
    
    const [currentComponent,setCurrentComponent] = useState(null)
    const [itemsQueue,setItemsQueue] = useState([]);

    const addToQueue = (itemToAdd) => {
        setItemsQueue(prevState =>[ itemToAdd,...prevState])
    }

    const handleClick = () =>
    {
        console.log("State is:" + state)
        setState(state+1);
    }


  return (
    <Card sx={{ maxWidth: 345 }}>
      <CardHeader
        avatar={
          <PersonIcon>
            
          </PersonIcon>
        }
        action={
          <IconButton aria-label="settings" onClick  = {handleClick}>
            <MoreVertIcon  />
          </IconButton>
        }
        title="Raviv"
        subheader="Participant"
      />

      <CardContent>
        <Typography variant="body2" color="text.secondary">
        <Box
      sx={{
        width: 300,
        height: 300,
        backgroundColor: '#bdbdbd',
       
      }}
    />  
            <Question text={state}/>
        </Typography>
      </CardContent>


    </Card>
  );
}
