import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class MatchsValidator {
    
    // Regex patterns for validating inputs
    private static final Pattern PATTERN_NUMERIC = Pattern.compile("\\d+");
    private static final Pattern PATTERN_QUARTERS = Pattern.compile("\\d{1,2}");
    private static final Pattern PATTERN_EVENT_TIME = Pattern.compile("\\d{2}\\.\\d{2}\\.\\d{4}-\\d{2}:\\d{2}");
    private static final Pattern PATTERN_TEAM = Pattern.compile("\\w{1,50}");

    public static boolean validateEventTimeUTC(String eventTimeUTC) {
        Matcher matcher = PATTERN_NUMERIC.matcher(eventTimeUTC);
        return matcher.matches();
    }

    public static boolean validateEventTime(String eventTime) {
        Matcher matcher = PATTERN_EVENT_TIME.matcher(eventTime);
        return matcher.matches();
    }

    public static boolean validateTeamName(String teamName) {
        Matcher matcher = PATTERN_TEAM.matcher(teamName);
        return matcher.matches();
    }

    public static boolean validateQuarter(String quarter) {
        Matcher matcher = PATTERN_QUARTERS.matcher(quarter);
        return matcher.matches();
    }

    public static boolean validateInput(String eventTimeUTC, String eventTime, String homeTeam, String awayTeam,
        String quarter1Home, String quarter2Home, String quarter3Home, String quarter4Home, String overtimeHome,
        String quarter1Away, String quarter2Away, String quarter3Away, String quarter4Away, String overtimeAway) {

        // Validate inputs
        if (!validateEventTimeUTC(eventTimeUTC)) {
            return false;
        }
        if (!validateEventTime(eventTime)) {
            return false;
        }
        if (!validateTeamName(homeTeam)) {
            return false;
        }
        if (!validateTeamName(awayTeam)) {
            return false;
        }
        if (!validateQuarter(quarter1Home)) {
            return false;
        }
        if (!validateQuarter(quarter2Home)) {
            return false;
        }
        if (!validateQuarter(quarter3Home)) {
            return false;
        }
        if (!validateQuarter(quarter4Home)) {
            return false;
        }
        if (overtimeHome != null && !validateQuarter(overtimeHome)) {
            return false;
        }
        if (!validateQuarter(quarter1Away)) {
            return false;
        }
        if (!validateQuarter(quarter2Away)) {
            return false;
        }
        if (!validateQuarter(quarter3Away)) {
            return false;
        }
        if (!validateQuarter(quarter4Away)) {
            return false;
        }
        if (overtimeAway != null && !validateQuarter(overtimeAway)) {
            return false;
        }

        return true;
    }
}
