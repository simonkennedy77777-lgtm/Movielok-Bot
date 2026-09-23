import os

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "")

USDT_BEP20 = os.environ.get("USDT_BEP20", "YOUR_BEP20_ADDRESS")
USDT_TRC20 = os.environ.get("USDT_TRC20", "YOUR_TRC20_ADDRESS")
BTC_ADDRESS = os.environ.get("BTC_ADDRESS", "YOUR_BTC_ADDRESS")

ADMIN_USERNAME = os.environ.get(
    "ADMIN_USERNAME",
    "@Movielokadmin"
)


# =========================
# MAIN MENU
# =========================

def main_menu():
    keyboard = [
        [InlineKeyboardButton("💎 Membership", callback_data="membership")],
        [InlineKeyboardButton("🆕 New Release", callback_data="new_release")],
        [InlineKeyboardButton("👥 Referral", callback_data="referral")],
        [InlineKeyboardButton("🆘 Help", callback_data="help")],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================
# MEMBERSHIP MENU
# =========================

def membership_menu():
    keyboard = [
        [InlineKeyboardButton("🆓 Free", callback_data="free")],
        [InlineKeyboardButton("💳 Paid", callback_data="paid")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_main")],
    ]

    return InlineKeyboardMarkup(keyboard)


def paid_menu():
    keyboard = [
        [InlineKeyboardButton("📅 Weekly Access — $3.99",
                              callback_data="weekly")],
        [InlineKeyboardButton("📅 Annual Access — $49.99",
                              callback_data="annual")],
        [InlineKeyboardButton("⭐ Special Access — $199.99",
                              callback_data="special")],
        [InlineKeyboardButton("🔙 Back", callback_data="membership")],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================
# PAYMENT MENU
# =========================

def payment_menu(plan):
    keyboard = [
        [
            InlineKeyboardButton(
                "USDT",
                callback_data=f"usdt_{plan}"
            )
        ],
        [
            InlineKeyboardButton(
                "BTC",
                callback_data=f"btc_{plan}"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="paid"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def usdt_menu(plan):
    keyboard = [
        [
            InlineKeyboardButton(
                "USDT BEP-20",
                callback_data=f"bep20_{plan}"
            )
        ],
        [
            InlineKeyboardButton(
                "USDT TRC-20",
                callback_data=f"trc20_{plan}"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data=f"payment_{plan}"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "🎬 <b>Welcome to Movie Bot</b>\n\n"
        "Choose an option from the menu below."
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=main_menu()
    )


# =========================
# BUTTON HANDLER
# =========================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    data = query.data

    # ---------------------
    # MAIN MENU
    # ---------------------

    if data == "back_main":

        await query.edit_message_text(
            "🎬 <b>Main Menu</b>",
            parse_mode="HTML",
            reply_markup=main_menu()
        )

    # ---------------------
    # MEMBERSHIP
    # ---------------------

    elif data == "membership":

        await query.edit_message_text(
            "💎 <b>Membership</b>\n\n"
            "Choose your membership option:",
            parse_mode="HTML",
            reply_markup=membership_menu()
        )

    # ---------------------
    # FREE MEMBERSHIP
    # ---------------------

    elif data == "free":

        text = (
            "🆓 <b>Free Membership</b>\n\n"
            "To become eligible for free access, "
            "complete the referral requirements.\n\n"
            "Your referral progress will be shown here "
            "once the referral system is connected."
        )

        keyboard = [
            [InlineKeyboardButton(
                "👥 My Referral",
                callback_data="referral"
            )],
            [InlineKeyboardButton(
                "🔙 Back",
                callback_data="membership"
            )],
        ]

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ---------------------
    # PAID
    # ---------------------

    elif data == "paid":

        await query.edit_message_text(
            "💳 <b>Paid Membership</b>\n\n"
            "Choose an access period:",
            parse_mode="HTML",
            reply_markup=paid_menu()
        )

    # ---------------------
    # PLANS
    # ---------------------

    elif data in ["weekly", "annual", "special"]:

        names = {
            "weekly": "Weekly Access — $3.99",
            "annual": "Annual Access — $49.99",
            "special": "Special Access — $199.99",
        }

        await query.edit_message_text(
            f"💳 <b>{names[data]}</b>\n\n"
            "Choose your payment method:",
            parse_mode="HTML",
            reply_markup=payment_menu(data)
        )

    # ---------------------
    # PAYMENT
    # ---------------------

    elif data.startswith("payment_"):

        plan = data.replace("payment_", "")

        await query.edit_message_text(
            "💰 <b>Select Payment Method</b>",
            parse_mode="HTML",
            reply_markup=payment_menu(plan)
        )

    # ---------------------
    # USDT
    # ---------------------

    elif data.startswith("usdt_"):

        plan = data.replace("usdt_", "")

        await query.edit_message_text(
            "💵 <b>USDT Payment</b>\n\n"
            "Choose the network:",
            parse_mode="HTML",
            reply_markup=usdt_menu(plan)
        )

    # ---------------------
    # BEP20
    # ---------------------

    elif data.startswith("bep20_"):

        plan = data.replace("bep20_", "")

        text = (
            "💵 <b>USDT BEP-20</b>\n\n"
            f"<code>{USDT_BEP20}</code>\n\n"
            "⚠️ Send USDT only through the BEP-20 network.\n\n"
            "After completing the payment, press "
            "<b>Payment Done ✅</b>."
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "✅ Payment Done",
                    callback_data=f"paid_done_{plan}_bep20"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data=f"usdt_{plan}"
                )
            ],
        ]

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ---------------------
    # TRC20
    # ---------------------

    elif data.startswith("trc20_"):

        plan = data.replace("trc20_", "")

        text = (
            "💵 <b>USDT TRC-20</b>\n\n"
            f"<code>{USDT_TRC20}</code>\n\n"
            "⚠️ Send USDT only through the TRC-20 network.\n\n"
            "After completing the payment, press "
            "<b>Payment Done ✅</b>."
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "✅ Payment Done",
                    callback_data=f"paid_done_{plan}_trc20"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data=f"usdt_{plan}"
                )
            ],
        ]

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ---------------------
    # BTC
    # ---------------------

    elif data.startswith("btc_"):

        plan = data.replace("btc_", "")

        text = (
            "₿ <b>Bitcoin Payment</b>\n\n"
            f"<code>{BTC_ADDRESS}</code>\n\n"
            "⚠️ Send BTC only to this Bitcoin address.\n\n"
            "After completing the payment, press "
            "<b>Payment Done ✅</b>."
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "✅ Payment Done",
                    callback_data=f"paid_done_{plan}_btc"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data=f"payment_{plan}"
                )
            ],
        ]

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ---------------------
    # PAYMENT DONE
    # ---------------------

    elif data.startswith("paid_done_"):

        parts = data.split("_")

        plan = parts[2]
        network = parts[3]

        user = query.from_user

        text = (
            "✅ <b>Payment Submitted</b>\n\n"
            "Your payment notification has been submitted "
            "for verification.\n\n"
            "Please wait for confirmation from the admin."
        )

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🔙 Main Menu",
                        callback_data="back_main"
                    )
                ]
            ])
        )

        # Notify admin
        if ADMIN_CHAT_ID:

            admin_text = (
                "💰 <b>Payment Notification</b>\n\n"
                f"👤 User: {user.full_name}\n"
                f"🆔 ID: <code>{user.id}</code>\n"
                f"📦 Plan: {plan}\n"
                f"💳 Network: {network}\n"
                f"🔗 Username: @{user.username}"
                if user.username
                else
                f"💰 <b>Payment Notification</b>\n\n"
                f"👤 User: {user.full_name}\n"
                f"🆔 ID: <code>{user.id}</code>\n"
                f"📦 Plan: {plan}\n"
                f"💳 Network: {network}"
            )

            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=admin_text,
                parse_mode="HTML"
            )

    # ---------------------
    # NEW RELEASE
    # ---------------------

    elif data == "new_release":

        keyboard = [
            [
                InlineKeyboardButton(
                    "🆕 Open New Releases",
                    url="https://t.me/YOUR_CHANNEL"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data="back_main"
                )
            ]
        ]

        await query.edit_message_text(
            "🆕 <b>New Releases</b>\n\n"
            "Tap the button below to open the channel.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ---------------------
    # REFERRAL
    # ---------------------

    elif data == "referral":

        bot_username = (
            await context.bot.get_me()
        ).username

        referral_link = (
            f"https://t.me/{bot_username}"
            f"?start=ref_{query.from_user.id}"
        )

        text = (
            "👥 <b>Referral Program</b>\n\n"
            "Invite your friends using your personal referral link.\n\n"
            f"🔗 <code>{referral_link}</code>\n\n"
            "Your referral statistics will appear here "
            "once the full referral database is connected."
        )

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🔙 Back",
                        callback_data="back_main"
                    )
                ]
            ])
        )

    # ---------------------
    # HELP
    # ---------------------

    elif data == "help":

        await query.edit_message_text(
            "🆘 <b>Help</b>\n\n"
            "For assistance, contact the admin:\n\n"
            f"{ADMIN_USERNAME}",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🔙 Back",
                        callback_data="back_main"
                    )
                ]
            ])
        )


# =========================
# RUN BOT
# =========================

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    PORT = int(os.environ.get("PORT", "10000"))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

if WEBHOOK_URL:
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="telegram",
        webhook_url=f"{WEBHOOK_URL.rstrip('/')}/telegram",
        drop_pending_updates=True,
    )
else:
    app.run_polling()


if __name__ == "__main__":
    main()
