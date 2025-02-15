
  
 export default function Page() {
  const associations = [
      {
          category: "Sport",
          name: "ATTAP Association de tennis de Table",
          address: "1 place du souvenir 91740 PUSSAY",
          contacts: ["06 76 33 78 44 (René LECLERE)", "06 28 79 94 27 (Noël GOURSILLAUD)"],
          mail:"rene.leclere4@orange.fr",
          website:"https://attapofficiel.wordpress.com/linscription-a-lattap/",
      },
      {
          category: "Sport",
          name: "Binouze runners",
          address: "10 Rue de la Beauce 91740 PUSSAY",
          contacts: ["06 21 53 42 59"],
          mail:"binouze.runners2891@gmail.com",
          website:"https://www.facebook.com/binouserunners/",
      },
      {
          category: "Culturelles",
          name: "Coup d'théatre",
          address: "Mairie de Pussay Place du jeu de Paume 91740 PUSSAY",
          contacts: ["06 16 11 18 96"],
          mail:"mulardchantal@gmail.com",
          website:"https://www.facebook.com/people/Coup-dth%C3%A9%C3%A2tre-Pussay/100041946253053/?_rdr",
      },
      {
          category: "Culturelles",
          name: "Cocktail des îles",
          address: "1 Impasse du Parc 91740 PUSSAY",
          contacts: ["06 62 29 62 51"],
          mail:"guylaine-tresor1@hotmail.fr",
      },
      {
          category: "Sociales et Solidaires",
          name: "Amicale des sapeurs-pompiers",
          address: "CENTRE DE SECOURS Place de l'Eglise 91740 PUSSAY",
          contacts: ["06 74 00 77 23"],
          mail:"florianlegorbelec@orange.fr",
          website:"https://www.facebook.com/people/Amicale-Sapeurs-Pompiers-De-Pussay/pfbid02EczUWZ8E3fH8weqWff4yFSgVX2UgV9Yy6wuet8yksJvCLVtvvU4m3Hw3vAEyQxJTl/?locale=fr_FR",
      },
      {
          category: "Sociales",
          name: "Les petites marmottes",
          address: "Mairie de Pussay place du jeu de paume 91740 PUSSAY",
          contacts: ["06 67 43 22 07"],
          mail:"airault.gisele@gmail.com",
          website:"https://www.instagram.com/bibliopussay/reel/DFLi1E-IB7f/",
      },
      {
          category: "Environnementales",
          name: "Agitons le local",
          address: "Mairie de Pussay Place du Jeu de Paume 91740 PUSSAY",
          contacts: ["06 95 13 29 95"],
          mail:"coucou@agitonslelocal.fr",
          website:"https://www.helloasso.com/associations/agitons-le-local",
      },
      {
          category: "Environnementales",
          name: "Aux légumes de Gaïa",
          address: "5D Route de Thionville 91745 PUSSAY",
          contacts: ["06 95 13 29 95"],
          mail:"amapdepussay@gmail.com",
          website: "https://amapdepussay.wixsite.com/aux-legumes-de-gaia",
      }
  ];

  return (
      <div style={{ fontFamily: "Arial, sans-serif", backgroundColor: "#f5f5f5", padding: "20px" }}>
          <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "space-around" }}>
              {associations.map((assoc, index) => (
                  <div key={index} style={{
                      background: "#fff",
                      padding: "20px",
                      width: "40%",
                      margin: "10px",
                      boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)",
                      borderRadius: "8px"
                  }}>
                      <div style={{ color: "#E65100", fontWeight: "bold" }}>{assoc.category}</div>
                      <h2 style={{ color: "#37474F" }}>{assoc.name}</h2>
                      <p>{assoc.address}</p>
                      {assoc.contacts.map((contact, i) => (
                          <p key={i}>📞 {contact}</p>
                      ))}
                      <div>
                      {assoc.mail && (
                          <a href={`mailto:${assoc.mail}`} style={buttonStyle}>Courriel</a>
			)}
			{assoc.website && (
                          <a href={assoc.website} target="_blank" rel="noopener noreferre" style={buttonStyle}>Site web</a>
		  	)}
			<a href={`#${assoc.name.replace(/\s+/g,"-").toLowerCase()}`} style={buttonStyle}>voir la fiche</a>
                      </div>
                  </div>
              ))}
          </div>
      </div>
  );
}

const buttonStyle = {
  display: "block",
  backgroundColor: "#FF5730",
  color: "white",
  textAlign: "center",
  padding: "10px",
  margin: "5px 0",
  textDecoration: "none",
  borderRadius: "5px",
};

