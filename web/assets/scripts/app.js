fetch('http://localhost:5000/flashcards/anglais').then(function(response) {
  return response.json();
}).then(function(data) {
  console.log(data.cards[0]);

      data.cards.forEach(function (card) {
          var title = card[1];
          var theme = card[4];
          var info = card[2] + " : " + card[3];

          // create section
          var card = document.createElement('section');
          card.className = 'Card card';

          // Now create content
          var cardContent = document.createElement('div');
          cardContent.className = 'card-content';

          // Now create card word
          var cardWord = document.createElement('div');
          cardWord.className = 'card-title';
          cardWord.innerHTML = title;
          cardContent.appendChild(cardWord);

          // Now create card theme
          var cardTheme = document.createElement('div');
          cardTheme.className = 'card-subtitle';
          cardTheme.innerHTML = theme;
          cardContent.appendChild(cardTheme);

          // Now create card description
          var cardDesc = document.createElement('div');
          cardDesc.className = 'card-info';
          var cardDescSpan = document.createElement('span');
          cardDescSpan.innerHTML = info;
          cardDesc.appendChild(cardDescSpan);
          cardContent.appendChild(cardDesc);

          card.appendChild(cardContent);

          // Now create card action
          var cardAction = document.createElement('div');
          cardAction.className = 'card-action';
          var cardEdit = document.createElement('a');
          cardEdit.innerHTML = "Edit"
          cardAction.appendChild(cardEdit);
          card.appendChild(cardAction);

          // insert into main
          document.getElementsByTagName('main')[0].appendChild(card);
      });
});
