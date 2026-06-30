import discord


class ConfirmView(discord.ui.View):
    def __init__(self, action):
        super().__init__(timeout=60)

        self.action = action
        self.value = None

    @discord.ui.button(
        label="Confirmer",
        emoji="✅",
        style=discord.ButtonStyle.green
    )
    async def confirm(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        try:

            self.action()

            embed = discord.Embed(
                title="✅ Succès",
                description="Action exécutée avec succès.",
                color=discord.Color.green()
            )

        except Exception as e:

            embed = discord.Embed(
                title="❌ Erreur",
                description=f"```{e}```",
                color=discord.Color.red()
            )

        self.disable_all_items()

        await interaction.response.edit_message(
            embed=embed,
            view=self
        )

    @discord.ui.button(
        label="Annuler",
        emoji="❌",
        style=discord.ButtonStyle.red
    )
    async def cancel(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        embed = discord.Embed(
            title="❌ Action annulée",
            color=discord.Color.orange()
        )

        self.disable_all_items()

        await interaction.response.edit_message(
            embed=embed,
            view=self
        )