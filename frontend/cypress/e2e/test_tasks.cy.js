describe('Checking task functionality', () => {
    // define variables that we need on multiple occasions
    let uid // user id
    let name // name of the user (firstName + ' ' + lastName)
    let email // email of the user

    let task_title = 'Test task'
    let view_key = 'dQw4w9WgXcQ'
    let todo_title = 'Test todo item'
  
    before(() => {
        cy.fixture('user.json')
          .then((user) => {
            cy.request({
              method: 'POST',
              url: 'http://localhost:5000/users/create',
              form: true,
              body: user
            }).then((response) => {
              uid = response.body._id.$oid;
              name = user.firstName + ' ' + user.lastName;
              email = user.email;

              cy.visit('http://localhost:3000')
              cy.contains('div', 'Email Address').type(email)
                cy.get('form')
                    .submit()
        
              cy.contains('div', 'Title')
                .find('input[type=text]').type(task_title)
              cy.contains('div', 'YouTube URL')
                .find('input[type=text]').type(view_key)
              cy.get('form')
                .submit()
            });
          });
      });
    
  
    beforeEach(function () {
      // enter the main main page
      cy.visit('http://localhost:3000')
      cy.contains('div', 'Email Address').type(email)
        cy.get('form')
            .submit()

      cy.contains('div', task_title).click()

    })
  
    it('create new todo item', () => {

      cy.contains('div.popup', task_title)
        .should('contain.text', task_title) 
        .find('form') 
        .find('input[type=text]') // Find the input field
        .should('exist') // Ensure the input field exists
        .type(todo_title); // Type the new todo item
  
      // Submit the form
      cy.contains('div.popup', task_title)
        .find('form.inline-form')
        .submit();
  
      // Assert that the new todo item exists in the list
      cy.contains('li.todo-item', todo_title).should('exist');

      cy.get('ul.todo-list')
        .find('li.todo-item')
        .last() 
        .should('contain.text', todo_title);

  });

    it('create todo item if description is empty', () => {
      // Locate the input field for the new todo item within the popup
      cy.contains('div.popup', task_title)
        .should('contain.text', task_title) 
        .find('form') 
        .find('input[type=text]') 
        .should('exist') 
  
      // Submit the form
      cy.contains('div.popup', task_title)
        .find('form.inline-form')
        .find('input[type=submit]')
        .should('be.disabled');
    });

    it('change status of todo item', () => {
      // Locate the checkbox for the todo item within the popup
      cy.contains('div.popup', task_title)
        .should('contain.text', task_title) 
        .find('ul.todo-list')
        .find('li.todo-item')
        .last()
        .find('span.checker') 
        .should('exist') 
        .click() // Click the checkbox to change its status
  
      // Assert that the status of the todo item has changed
      cy.contains('div.popup', task_title)
        .find('ul.todo-list')
        .find('li.todo-item')
        .last()
        .find('span') 
        .should('have.class', 'checker checked');

        cy.contains('div.popup', task_title)
        .should('contain.text', task_title) 
        .find('ul.todo-list')
        .find('li.todo-item')
        .last()
        .find('span.checker') 
        .should('exist') 
        .click() // Click the checkbox to change its status
  
      // Assert that the status of the todo item has changed
      cy.contains('div.popup', task_title)
        .find('ul.todo-list')
        .find('li.todo-item')
        .last()
        .find('span') 
        .should('have.class', 'checker unchecked');
    });

    it('delete todo item', () => {
      // Locate the delete button for the todo item within the popup
      cy.contains('div.popup', task_title)
        .should('contain.text', task_title) 
        .find('ul.todo-list')
        .find('li.todo-item')
        .last()
        .find('span.remover') 
        .should('exist') 
        .click() // Click the delete button to remove the todo item
  
      // Assert that the todo item has been removed from the list
      cy.contains('div.popup', task_title)
        .find('ul.todo-list')
        .find('li.todo-item').contains(todo_title)
        .should('not.exist');
    });
      
    after(function () {
      // clean up by deleting the user from the database
      cy.request({
        method: 'DELETE',
        url: `http://localhost:5000/users/${uid}`
      }).then((response) => {
        cy.log(response.body)
      })
    })
  })