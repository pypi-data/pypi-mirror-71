    addRow: function() {
      let name    = this.newRow.name.trim().toLowerCase();
      let surname = this.newRow.command.trim().toLowerCase();
      if (name && surname) {  
        this.rows.push({
          id:      this.rows.length,
          name:    name,
          surname: surname
        });
        this.sortDir = 'desc'; this.sortBy('id'); // Default sorting
      }
      this.newRow.name = this.newRow.command = '';
    },


  <h2>New Row 😊</h2>
  <form v-on:submit.prevent="addRow">
    <input type="text" v-model="newRow.name" placeholder="Name" required>
    <input type="text" v-model="newRow.command" placeholder="Command" required>
    <button type="submit" class="btn">Add row</button>
  </form>

