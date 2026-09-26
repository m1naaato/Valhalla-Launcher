// priority: -500

/*
 * Author: vyrriox
 * Description: Script dedicated to modifying item statistics such as attack speed or damage.
 * Note: ItemEvents.modification MUST be in startup_scripts.
 */

ItemEvents.modification(event => {
    /*
     * I need to increase the attack speed of the spear from Choccos Mobs.
     * Reverting to simple property modification now that the script is correctly in startup_scripts.
     */

    // Create Diesel Generators Hammer Durability
    event.modify('createdieselgenerators:hammer', item => {
        item.maxDamage = 14
    })
})
