import React from 'react';
import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';
import { Box } from '@mui/system';
import randomNormal from 'random-normal';

export default function ShortuctsMenu(props){
    var randomNormal = require('random-normal');

    const handleClick = (role) => {
        const gender = Math.floor(Math.random() * 2) ==0? "male": "female"
        const name = gender ==="male" ?male_names[Math.floor(Math.random() * male_names.length)] :female_names[Math.floor(Math.random() * female_names.length)]
    props.set_user({"name": name, "role":role,"sex":gender, "age": Math.floor(randomNormal({mean:30,dev:15}) )+ 18,"id":  makeid(7)})
    };
    const shortcuts = ["doctor" ,"nurse","lab technician", "investigator", "participant",]

    return (
        <div>
            Fast Registeraion:

            <Box sx={{marginTop:"10px"}}>
            <Stack sx={{flexWrap:"wrap"}} direction="row" spacing={1}>
                <Box sx={{margin:"-10px"}}>
            {shortcuts.map(role =><Chip label={role} name={role} onClick={()=>handleClick(role)} sx={{flex: "1 1 160px",
        margin: "4px"}}/>)}
            </Box>
            </Stack>
            </Box>
        </div>
    )
}


function ClickableChips() {
    const handleClick = () => {
        fetch('http://names.drycodes.com/10?nameOptions=girl_names', {
            // configuration
         })
         .then(response => response.json())
         .then(response => {
             console.log(response)
         })
    };
  
    return (
      <Stack direction="row" spacing={1}>
        <Chip label="Clickable" onClick={handleClick} />
      </Stack>
    );
  }



  const makeid = (length) =>  {
    var result           = '';
    var characters       = '123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * 
 charactersLength));
   }
   return parseInt(result);
}
const female_names =  [
    "Pearl Bailey",
    "Adriana Ashlie",
    "Lorelei Paula",
    "Lupita Bailey",
    "Lana Sadie",
    "Candace Milena",
    "Trixy Kit",
    "Marilyn Rosa",
    "Liza Delany",
    "River Shelly",
    "Cristina Krystal",
    "Rhiannon Deedee",
    "Fifi Adele",
    "Mathilde Malinda",
    "Leyla Holly",
    "Teagan Deb",
    "Shauna Carley",
    "Gemma Ainsley",
    "Charlize Habiba",
    "Siobhan Ashley",
    "Oasis Tracie",
    "Debra Destiny",
    "Princess Elektra",
    "Madonna Kaidence",
    "Alanis Jessa",
    "Faith Tracy",
    "January Annmarie",
    "Cami Bridget",
    "Delaney Reanna",
    "Enya Jean",
    "Acacia Xena",
    "Leigh Nikita",
    "Carys Evaline",
    "Beatrix Andromeda",
    "Sophia Tia",
    "Regina Naja",
    "Millicent Anastasia",
    "Gracie Leila",
    "Charmaine Beverly",
    "Zena Eris",
    "Oona Cressida",
    "Jaylinn Alyssia",
    "Madeline Kimberlee",
    "Asma Dede",
    "Sylvie Lena",
    "Gwyneth Jena",
    "Griselda Genesis",
    "Kayley Tracey",
    "Lilita Melinda",
    "Pauline Goldie",
    "Chanelle Jenny",
    "Dolly Nadia",
    "Chris Genna",
    "Magdalena Rachael",
    "Janessa Odette",
    "Carenza Honor",
    "Nadine Taryn",
    "Lindy Margo",
    "Modesty Ronda",
    "Kalia Michelle",
    "Isha Raine",
    "Carter Tracy",
    "Allie Wendy",
    "Renae Tina",
    "Karolina Caterina",
    "Melina Dena",
    "Larissa Millicent",
    "Harmony Dionne",
    "Cierra Lucia",
    "Guadalupe Brea",
    "Charlize Theodora",
    "Lesly Mya",
    "Sybil Amy",
    "Jacinta Katarina",
    "Shari Yvonne",
    "Kera Anamaria",
    "Jaqueline Orianna",
    "Anisa Leyla",
    "Theresa Isa",
    "Leona Milly",
    "Isabell Adele",
    "Mercedes Camilla",
    "Sophy Jeanine",
    "Leena Christie",
    "Cici Danica",
    "Rowan Deann",
    "Keana Kat",
    "Adelynn Kourtney",
    "Hazel Adelene",
    "Rhoda Zada",
    "Cerys Vera",
    "Keri Gemma",
    "Anisa Chris",
    "Odele Daina",
    "Susan Tisha",
    "Kirstin Lucia",
    "Dolores Taryn",
    "Christie Cassidy",
    "Kinsley Kasey",
    "Natalia Sascha"
    ]
const male_names=[
    "Ciaran Oisin",
    "Nevin Ernest",
    "Leonardo Gunner",
    "Julian Keith",
    "Kellan Marik",
    "Dermot Salvatore",
    "Jedidiah York",
    "Finbar Abel",
    "Glynn Django",
    "Chas Johnathan",
    "Malcolm Norbert",
    "Yuri Archer",
    "Archie Quinn",
    "Ryder Tiger",
    "Adriel Phil",
    "Bear Cyrus",
    "Lloyd Harvey",
    "Barclay Clinton",
    "Solomon Sasha",
    "Daire Trace",
    "Dalton Steven",
    "Jon Branden",
    "Isidore Pierce",
    "Jared Brooks",
    "Joshua Johnathan",
    "Freddy Blaine",
    "Reynaldo Kendrick",
    "Ken Egon",
    "Castor Emanuel",
    "Jaylon Tim",
    "Stefan Josh",
    "Sandy Elijah",
    "Karl Darren",
    "Blain Salman",
    "Casper Lukas",
    "Geoff Callum",
    "Elijah Niall",
    "Malik Jett",
    "Chaz Linden",
    "Pierce Felix",
    "Nestor Elijah",
    "Terence Salvador",
    "Nik Sol",
    "Kyan Vishal",
    "Ansel Edwin",
    "Curtis Dominick",
    "Piers Charley",
    "Cyrus Conan",
    "Maverick Tucker",
    "Jago Jedidiah",
    "Merick Cyrus",
    "Toryn Jedediah",
    "Matthias Garth",
    "Kingston Yehudi",
    "Donovan Maison",
    "Jorge Leslie",
    "Carson Donald",
    "Mervin Quintrell",
    "Forrest Jessie",
    "Cesar Jude",
    "Deon Brady",
    "Alvin Emiliano",
    "Zayden Carey",
    "Alaric Dillon",
    "Igor Arlo",
    "Remy Burton",
    "Vivian Clay",
    "Brock Cuthbert",
    "Beau Larry",
    "Ezio Tiberius",
    "Rodney Sandeep",
    "Doyle Aldo",
    "Ellington Randolph",
    "Humberto Alec",
    "Flynn Rodrigo",
    "Kedrick Haiden",
    "Wesley Rick",
    "Larry Geraint",
    "Dakota Tod",
    "Stacey Evan",
    "Jody Stone",
    "Kerry Sherman",
    "Jefferson Ari",
    "Eustace Ray",
    "Jesse Cillian",
    "Jak Troy",
    "Ellis Wyatt",
    "Trey Caydon",
    "Abriel Zach",
    "Sven Nathan",
    "Francesco Adriel",
    "Ignacio Joe",
    "Ade Oscar",
    "Joseph Albany",
    "George Zayn",
    "Shadrach Laurence",
    "Justice Gabe",
    "Manny Yahir",
    "Mario Ryland",
    "Gabe Linden"
    ]